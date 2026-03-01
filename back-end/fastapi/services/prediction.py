import shap
import numpy as np
import pandas as pd
import xgboost as xgb
from langchain_core.messages import SystemMessage, HumanMessage
from repositories.prediction import IPredictionRepository
from services.llm import LLMService
from value_objects.prediction import IPrediction, Prediction
from value_objects.population import TotalPopulation
from value_objects.income import MedianIncome
from value_objects.radar import Radar
from value_objects.operation import Operation

class PredictionService:
    def __init__(self, prediction_repository: IPredictionRepository, llm_service: LLMService):
        self.prediction_repository = prediction_repository
        self.llm_service = llm_service
        self.feature_importance = None
        self.negative_importance_features = []
        self.feature_name_map = {
            '競爭優勢': '區域市占率',
            'people_per_store': '店均服務人數',
            '競爭壓力指標': '競爭飽和度',
            '最近的熱鬧據點距離': '最近導流節點距離',
            '發票張數指標': '發票張數指標',
            '租金_log': '租金',
            '里人均收入中位數': '人均收入',
            '里人口數': '基礎客源',
            '日夜人流差': '商圈日夜落差',
            '發票銷售額指標': '發票銷售指標',
            '行政區平日日間活動人數': '日間活動人流'
        }
        self._calculate_feature_importance()
    
    def _calculate_feature_importance(self):
        # 1. 準備資料與計算 SHAP
        fields = self.prediction_repository.get_prediction_features()
        prediction_table = self.prediction_repository.get_prediction_table()
        data = prediction_table[fields].copy()
        # 類別型轉碼以利計算
        for col in data.select_dtypes(['category']).columns:
            data[col] = data[col].cat.codes
        explainer = shap.TreeExplainer(self.prediction_repository.get_prediction_model())
        shap_values = explainer.shap_values(data)
        shap_v = shap_values[1] if isinstance(shap_values, list) else shap_values
        # 2. 自動判定正負向邏輯
        analysis_data = []
        for i, col in enumerate(fields):
            importance = np.abs(shap_v[:, i]).mean()
            # 計算特徵值與其 SHAP 值的相關係數來判定方向
            correlation = np.corrcoef(data[col], shap_v[:, i])[0, 1]
            direction = "(+)" if correlation > 0 else "(-)"
            analysis_data.append({'Feature': col, 'Direction': direction, 'Importance': importance})
        # 3. 排序
        self.feature_importance = pd.DataFrame(analysis_data).sort_values(by='Importance', ascending=False)
        self.negative_importance_features = self.feature_importance[self.feature_importance['Direction'] == '(-)']['Feature'].tolist()
    
    def get_operation_score_from_model(self, city: str, district: str, neighborhood: str, brand_type: int) -> tuple[float, int]:
        fields = self.prediction_repository.get_prediction_features()
        data = self.prediction_repository.get_prediction_table_data_by_location(city=city, district=district, neighborhood=neighborhood)
        first_data = data.head(1)
        id = first_data["id"].iloc[0]
        data = first_data[fields].copy()
        data['是否便利商店'] = brand_type
        dmatrix = xgb.DMatrix(data, enable_categorical=True)
        operation_rate = self.prediction_repository.get_prediction_model().predict(dmatrix)
        operation_score = operation_rate * 100
        first_operation_score = operation_score[0]      
        return float(first_operation_score), int(id)

    def get_operation_report(self, score: float, brand_type: int) -> str:
        prob = score / 100
        threshold = 0.5 if brand_type == 1 else 0.7
        return "優質位點 (推薦展店)" if prob >= threshold else "高風險位點 (建議迴避)"

    def get_ai_insight(self, id: int, score: float, report: str) -> str:
        print("id", id)
        # 方式一: LLM
        row = self.prediction_repository.get_report_table_data_by_id(id)
        print(row)
        brand_type = "便利商店" if row['是否便利商店'] == 1 else "超市及藥妝"
        user_message = (
        f"你是一位精通雙北零售市場的資深顧問。請根據以下數據提供 60 字內中文評語。\n"
        f"【位點數據】：\n"
        f"- 縣市：{row['縣市']}\n"
        f"- 位置：{row['行政區']}{row['里別']}\n"
        f"- 區域人口：{row['里人口數']} 人 / 收入中位數：{row['里人均收入中位數']} 千元\n"
        f"- 業態：{brand_type}\n"
        f"- 預測分數：{score:.1f} (決策：{report})\n"
        f"- 影響指標 1：{row['top1_feature']} ({row['top1_dir']})\n"
        f"- 影響指標 2：{row['top2_feature']} ({row['top2_dir']})\n\n"
        f"【分析邏輯與顧問語氣準則】：\n"
        f"0. 絕對規模判定：若里人口數 < 2000，無論收入多高，優先判定為『商圈規模小，基礎客源支撐力不足』，此時不適用強勢商圈保護邏輯。"
        f"1. 體質防禦：新北市(人口>4800/收入>510k)或台北市(人口>5500/收入>670k)符合任一則判定為強勢商圈，禁止說體質差。\n"
        f"2. 專業轉化：將'核心據點距離優異'轉化為'位處人流聚集核心'；'租金壓力優異'轉化為'具備展店成本優勢'；'市占/飽和度弱'轉化為'品牌進入門檻顯著'。\n"
        f"3. 歸因策略：若分數低但體質強，應解讀為'市場競爭飽和'。若兩者皆低，則解讀為'基礎客源門檻未達'。\n"
        f"4. 市場規模補償：若人口 > 10,000 且分數低(<40)，絕不可否定商圈，必須解讀為'市場雖極具誘力，但品牌面臨飽和競爭或進入門檻限制'。\n"
        f"5. 藍海判定：若分數高(>60)且市占率弱，應解讀為'具備高度開發潛力之藍海商圈'。\n"
        f"\n【顧問語氣強度控制規則】：\n"
        f"6. 業態門檻感知：\n"
        f"   - 若為「便利商店」(門檻 50)：50-60 分應定位為『險勝』，語氣保守；60-80 分為『優質』，語氣正向；80 分以上為『極佳』。\n"
        f"   - 若為「超市及藥妝」(門檻 70)：70-75 分應定位為『險勝』，語氣保守且需強調成本控制；75-85 分為『優質』；85 分以上為『極佳』。\n"
        f"7. 針對「險勝」區間（如超市 71.9 分）：禁止使用『極力推薦』、『高潛力』，改用『具備基礎條件』、『建議審慎評估成本』。\n"
        f"8. 以'該位點...'開頭，禁提品牌與登記狀態，字數嚴控 60 字內。"
        )
        ai_insight = self.llm_service.invoke(user_message=user_message)

        # 方式二: 查表
        # ai_insight = self.prediction_repository.get_ai_insight_from_table(id)
        return ai_insight

    def get_radar(self, id: int = None, distinct: str = None, neighborhood: str = None, is_cvs: int = None, target_status: str = None, selected_idx: list[int] = None) -> Radar:
        # --- 1. 載入資料庫 ---
        shap_database = self.prediction_repository.get_shap_database()
        db = shap_database['lookup_table']
        # 關鍵修正：只保留數值型特徵，移除類別型欄位
        all_numeric_features = [f for f in shap_database['features'] if db[f].dtype != 'category' and db[f].dtype != 'object']
        group_key = 'CVS' if is_cvs == 1 else 'Super'
        thresholds_dict = shap_database[group_key]['thresholds']
        # --- 2. 資料篩選與定位 ---
        if id != None:
            mask = (db['id'] == id)
        else:
            mask = (db['行政區'] == distinct) & (db['里別'].str.contains(neighborhood)) & (db['是否便利商店'] == is_cvs)
        target_data = db[mask]
        if target_data.empty: return print(f"❌ 找不到資料：{distinct}{neighborhood}")
        if target_status:
            specific_data = target_data[target_data['登記現況'] == target_status]
            if specific_data.empty:
                return print(f"⚠️ 在 {distinct}{neighborhood} 找不到狀態為【{target_status}】的店點。")
            example_row = specific_data.iloc[0]
        else:
            example_row = target_data.iloc[0]
        # --- 3. 得分計算 (僅針對數值特徵) ---
        v_inverted, s_inverted, labels = [], [], []
        for feat in all_numeric_features:
            # 取得該特徵的 SHAP 絕對值
            v_val = np.abs(target_data[feat].mean())
            s_val = np.abs(example_row[feat])

            # 對照該特徵的分位數基準 (從字典中取出)
            feat_thresholds = thresholds_dict.get(feat, [0, 0, 0, 0])

            # 計算原始分位 (1-5分)
            v_orig = np.digitize(v_val, feat_thresholds) + 1
            s_orig = np.digitize(s_val, feat_thresholds) + 1

            # 負向反轉邏輯：如果是負向特徵，數值越高（影響越大）得分越低
            if feat in self.negative_importance_features:
                v_score = max(1, 6 - v_orig)
                s_score = max(1, 6 - s_orig)
                sign = "(-)"
            else:
                v_score = v_orig
                s_score = s_orig
                sign = "(+)"

            v_inverted.append(int(v_score))
            s_inverted.append(int(s_score))
            labels.append(f"{self.feature_name_map.get(feat, feat)}\n{sign}")
        # --- 4. 繪圖數據篩選 (如果使用者有指定 selected_idx) ---
        if selected_idx is not None:
            labels = [labels[i] for i in selected_idx]
            v_inverted = [v_inverted[i] for i in selected_idx]
            s_inverted = [s_inverted[i] for i in selected_idx]
        return Radar(labels=labels, values=s_inverted)
    
    def run_prediction(self, city: str, district: str, neighborhood: str, brand_type: int) -> IPrediction:
        try:
            score, id = self.get_operation_score_from_model(city, district, neighborhood, brand_type)
            report = self.get_operation_report(score, brand_type)
        
            return Prediction(
                operation=Operation(
                    score=score,
                    report=report
                ),
                total_population=TotalPopulation(
                    neighborhood=self.prediction_repository.get_neighborhood_total_population(city, district, neighborhood),
                    district=self.prediction_repository.get_district_total_population(city, district),
                ),
                median_income=MedianIncome(
                    neighborhood=self.prediction_repository.get_neighborhood_median_income(city, district, neighborhood),
                    district=self.prediction_repository.get_district_median_income(city, district),
                ),
                competitor_count=self.prediction_repository.get_competitor_count(city, district, neighborhood, brand_type),
                ai_insight=self.get_ai_insight(id, score, report),
                radar=self.get_radar(id=id, selected_idx=[1,2,3,4,6,9]),
                is_success=True
            )
        except Exception as e:
            print(e)
            return Prediction(
                operation=Operation(
                    score=0,
                    report=""
                ),
                total_population=TotalPopulation(
                    neighborhood=0,
                    district=0,
                ),
                median_income=MedianIncome(
                    neighborhood=0,
                    district=0,
                ),
                competitor_count=0,
                ai_insight=[],
                radar=Radar(
                    labels=[],
                    values=[],
                ),
                is_success=False
            )
import pandas as pd
import os
import pickle
from abc import ABC, abstractmethod
import xgboost as xgb
import numpy as np
import random
import shap
from common import TRAIN_TABLE_FILE_NAME, VALIDATION_TABLE_FILE_NAME, PREDICTION_TABLE_FILE_NAME, REPORT_TABLE_FILE_NAME, PREDICTION_MODEL_FILE_NAME, SHAP_DATABASE_FILE_NAME
from value_objects.radar import Radar

train_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{TRAIN_TABLE_FILE_NAME}"))
validation_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{VALIDATION_TABLE_FILE_NAME}"))
prediction_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{PREDICTION_TABLE_FILE_NAME}"))
report_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{REPORT_TABLE_FILE_NAME}"))
prediction_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "models", f"{PREDICTION_MODEL_FILE_NAME}"))
shap_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "models", f"{SHAP_DATABASE_FILE_NAME}"))

class IPredictionRepository(ABC):    
    @abstractmethod
    def get_operation_score_from_table(self, city: str, district: str, neighborhood: str, brand_type: int) -> float:
        pass
    
    @abstractmethod
    def get_operation_score_from_model(self, city: str, district: str, neighborhood: str, brand_type: int) -> tuple[float, int]:
        pass
    
    @abstractmethod
    def get_operation_report(self, score: float, brand_type: int) -> str:
        pass
    
    @abstractmethod
    def get_neighborhood_total_population(self, city: str, district: str, neighborhood: str) -> int:
        pass
    
    @abstractmethod
    def get_district_total_population(self, city: str, district: str) -> int:
        pass
    
    @abstractmethod
    def get_neighborhood_median_income(self, city: str, district: str, neighborhood: str) -> int:
        pass
    
    @abstractmethod
    def get_district_median_income(self, city: str, district: str) -> int:
        pass
    
    @abstractmethod
    def get_competitor_count(self, city: str, district: str, neighborhood: str, brand_type: int) -> int:
        pass
    
    @abstractmethod
    def get_ai_insight_from_table(self, id: int) -> str:
        pass
    
    @abstractmethod
    def get_radar(self, id: int = None, distinct: str = None, neighborhood: str = None, is_cvs: int = 1, target_status: str = None, selected_idx: list[int] = None) -> Radar:
        pass

class PredictionRepository(IPredictionRepository):
    def __init__(self):
        self.train_table = None
        self.validation_table = None
        self.prediction_table = None
        self.report_table = None
        self.prediction_model = None
        self.shap_database = None
        self.prediction_features = []
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
        self._run_data_preprocess()
        self._load_model()
        self._calculate_feature_importance()

    def _run_data_preprocess(self) -> pd.DataFrame:
        self.train_table = self._data_preprocess(pd.read_csv(train_table_file_path))
        self.validation_table = self._data_preprocess(pd.read_csv(validation_table_file_path))
        self.report_table = self._data_preprocess(pd.read_csv(report_table_file_path))
        try:
            self.prediction_table = pd.read_csv(prediction_table_file_path)
            self.prediction_table['最近的熱鬧據點類型'] = self.prediction_table['最近的熱鬧據點類型'].astype('category')
        except FileNotFoundError:
            concat_data = pd.concat([self.train_table, self.validation_table], ignore_index=True)
            concat_data.to_csv(prediction_table_file_path, index=False)
            print(f"Created prediction table file at {prediction_table_file_path}")
            self.prediction_table = concat_data

    def _load_model(self):
        with open(prediction_model_path, "rb") as f:
            pkl_data = pickle.load(f)
            self.prediction_model = pkl_data['model']
            self.prediction_features = pkl_data['features']
        with open(shap_database_path, "rb") as f:
            pkl_data = pickle.load(f)
            self.shap_database = pkl_data

    def _calculate_feature_importance(self):
        # 1. 準備資料與計算 SHAP
        fields = self.prediction_features
        data = self.prediction_table[fields].copy()
        # 類別型轉碼以利計算
        for col in data.select_dtypes(['category']).columns:
            data[col] = data[col].cat.codes
        explainer = shap.TreeExplainer(self.prediction_model)
        shap_values = explainer.shap_values(data)
        shap_v = shap_values[1] if isinstance(shap_values, list) else shap_values
        # 2. 自動判定正負向邏輯
        analysis_data = []
        for i, col in enumerate(self.prediction_features):
            importance = np.abs(shap_v[:, i]).mean()
            # 計算特徵值與其 SHAP 值的相關係數來判定方向
            correlation = np.corrcoef(data[col], shap_v[:, i])[0, 1]
            direction = "(+)" if correlation > 0 else "(-)"
            analysis_data.append({'Feature': col, 'Direction': direction, 'Importance': importance})
        # 3. 排序
        self.feature_importance = pd.DataFrame(analysis_data).sort_values(by='Importance', ascending=False)
        self.negative_importance_features = self.feature_importance[self.feature_importance['Direction'] == '(-)']['Feature'].tolist()

    def _data_preprocess(self, df_ml: pd.DataFrame) -> pd.DataFrame:
        df_ml['日夜人流差'] = df_ml['行政區平日日間活動人數'] - df_ml['行政區平日夜間停留人數']
        df_ml['租金_log'] = np.log1p(df_ml['租金'])
        df_ml['最近的熱鬧據點類型'] = df_ml['最近的熱鬧據點類型'].astype('category')
        return df_ml

    def get_operation_score_from_table(self, city: str, district: str, neighborhood: str, brand_type: int) -> float:
        fields = ["營運推薦分數"]
        query = (self.report_table["縣市"] == city) & (self.report_table["行政區"] == district) & (self.report_table["里別"] == neighborhood) & (self.report_table["是否便利商店"] == brand_type)
        data = self.report_table[query][fields]
        avg_score = data["營運推薦分數"].mean()
        return round(avg_score, 2)

    def get_operation_score_from_model(self, city: str, district: str, neighborhood: str, brand_type: int) -> tuple[float, int]:
        fields = self.prediction_features
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district) & (self.prediction_table["里別"] == neighborhood)
        first_data = self.prediction_table[query].head(1)
        id = first_data["id"].iloc[0]
        data = first_data[fields].copy()
        data['是否便利商店'] = brand_type
        dmatrix = xgb.DMatrix(data, enable_categorical=True)
        operation_rate = self.prediction_model.predict(dmatrix)
        operation_score = operation_rate * 100
        first_operation_score = operation_score[0]      
        return float(first_operation_score), int(id)

    def get_operation_report(self, score: float, brand_type: int) -> str:
        prob = score / 100
        threshold = 0.5 if brand_type == 1 else 0.7
        return "優質位點 (推薦展店)" if prob >= threshold else "高風險位點 (建議迴避)"

    def get_neighborhood_total_population(self, city: str, district: str, neighborhood: str) -> int:
        fields = ["里人口數"]
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district) & (self.prediction_table["里別"] == neighborhood)
        data = self.prediction_table[query][fields]
        neighborhood_total_population = int(data["里人口數"].iloc[0])
        return neighborhood_total_population

    def get_district_total_population(self, city: str, district: str) -> int:
        fields = ["縣市", "行政區", "里別", "里人口數"]
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district)
        data = self.prediction_table[query][fields].copy()
        district_total_population = int(data.drop_duplicates(subset=["里別"])["里人口數"].sum())
        return district_total_population

    def get_neighborhood_median_income(self, city: str, district: str, neighborhood: str) -> int:
        fields = ["里人均收入中位數"]
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district) & (self.prediction_table["里別"] == neighborhood)
        data = self.prediction_table[query][fields]
        neighborhood_median_income = int(data["里人均收入中位數"].iloc[0])
        return neighborhood_median_income

    def get_district_median_income(self, city: str, district: str) -> int:
        fields = ["縣市", "行政區", "里別", "里人均收入中位數"]
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district)
        data = self.prediction_table[query][fields].copy()
        district_median_income = data.drop_duplicates(subset=["里別"])["里人均收入中位數"].median()
        return int(district_median_income)

    def get_competitor_count(self, city: str, district: str, neighborhood: str, brand_type: int) -> int:
        fields = ["id"]
        query = (self.prediction_table["縣市"] == city) & (self.prediction_table["行政區"] == district) & (self.prediction_table["里別"] == neighborhood) & (self.prediction_table["是否便利商店"] == brand_type)
        data = self.prediction_table[query][fields]
        competitor_count = len(data)
        return competitor_count

    def get_ai_insight_from_table(self, id: int) -> str:
        fields = ["ai_review"]
        query = (self.report_table["id"] == id)
        data = self.report_table[query][fields]
        return data["ai_review"].iloc[0]

    def get_radar(self, id: int = None, distinct: str = None, neighborhood: str = None, is_cvs: int = None, target_status: str = None, selected_idx: list[int] = None) -> Radar:
        # --- 1. 載入資料庫 ---
        db = self.shap_database['lookup_table']
        # 關鍵修正：只保留數值型特徵，移除類別型欄位
        all_numeric_features = [f for f in self.shap_database['features'] if db[f].dtype != 'category' and db[f].dtype != 'object']
        group_key = 'CVS' if is_cvs == 1 else 'Super'
        thresholds_dict = self.shap_database[group_key]['thresholds']
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
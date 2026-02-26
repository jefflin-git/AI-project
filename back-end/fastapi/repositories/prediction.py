import pandas as pd
import os
import pickle
from abc import ABC, abstractmethod
import xgboost as xgb
import numpy as np
from common import TRAIN_TABLE_FILE_NAME, VALIDATION_TABLE_FILE_NAME, PREDICTION_TABLE_FILE_NAME, REPORT_TABLE_FILE_NAME, PREDICTION_MODEL_FILE_NAME, SHAP_DATABASE_FILE_NAME

train_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{TRAIN_TABLE_FILE_NAME}"))
validation_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{VALIDATION_TABLE_FILE_NAME}"))
prediction_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{PREDICTION_TABLE_FILE_NAME}"))
report_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{REPORT_TABLE_FILE_NAME}"))
prediction_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "models", f"{PREDICTION_MODEL_FILE_NAME}"))
shap_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "models", f"{SHAP_DATABASE_FILE_NAME}"))

class IPredictionRepository(ABC):    
    @abstractmethod
    def get_prediction_features(self) -> list:
        pass

    @abstractmethod
    def get_prediction_table(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_prediction_model(self) -> xgb.XGBClassifier:
        pass

    @abstractmethod
    def get_shap_database(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_data_by_location(self, city: str, district: str, neighborhood: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_operation_score_from_table(self, city: str, district: str, neighborhood: str, brand_type: int) -> float:
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

class PredictionRepository(IPredictionRepository):
    def __init__(self):
        self.train_table = None
        self.validation_table = None
        self.prediction_table = None
        self.report_table = None
        self.prediction_model = None
        self.shap_database = None
        self.prediction_features = []
        self._run_data_preprocess()
        self._load_model()
        self._set_indices()       

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

    def _data_preprocess(self, df_ml: pd.DataFrame) -> pd.DataFrame:
        df_ml['日夜人流差'] = df_ml['行政區平日日間活動人數'] - df_ml['行政區平日夜間停留人數']
        df_ml['租金_log'] = np.log1p(df_ml['租金'])
        df_ml['最近的熱鬧據點類型'] = df_ml['最近的熱鬧據點類型'].astype('category')
        return df_ml

    def _set_indices(self):
        # 建立索引以加速查詢
        self.prediction_table.set_index(['縣市', '行政區', '里別'], inplace=False)

    def get_prediction_features(self) -> list:
        return self.prediction_features
    
    def get_prediction_table(self) -> pd.DataFrame:
        return self.prediction_table
    
    def get_prediction_model(self) -> xgb.XGBClassifier:
        return self.prediction_model

    def get_shap_database(self) -> pd.DataFrame:
        return self.shap_database

    def get_data_by_location(self, city: str = None, district: str = None, neighborhood: str = None) -> pd.DataFrame:
        # 封裝底層查詢邏輯
        if city != None and district != None and neighborhood != None:
            query = (self.prediction_table["縣市"] == city) & \
                    (self.prediction_table["行政區"] == district) & \
                    (self.prediction_table["里別"] == neighborhood)
        elif city != None and district != None:
            query = (self.prediction_table["縣市"] == city) & \
                        (self.prediction_table["行政區"] == district)
        elif city != None:
            query = (self.prediction_table["縣市"] == city)
        data = self.prediction_table[query]
        if data.empty: raise ValueError("Location not found")
        return data
    
    def get_operation_score_from_table(self, city: str, district: str, neighborhood: str, brand_type: int) -> float:
        fields = ["營運推薦分數"]
        query = (self.report_table["縣市"] == city) & \
                    (self.report_table["行政區"] == district) & \
                    (self.report_table["里別"] == neighborhood) & \
                    (self.report_table["是否便利商店"] == brand_type)
        data = self.report_table[query][fields]
        avg_score = data["營運推薦分數"].mean()
        return round(avg_score, 2)

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
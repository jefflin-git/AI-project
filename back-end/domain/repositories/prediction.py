import pandas as pd
from abc import ABC, abstractmethod
import xgboost as xgb

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
    def get_predition_mapping(self) -> dict:
        pass

    @abstractmethod
    def get_shap_database(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_prediction_table_data_by_location(self, city: str, district: str, neighborhood: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_report_table_data_by_id(self, id: int) -> pd.DataFrame:
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
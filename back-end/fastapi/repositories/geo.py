import pandas as pd
import os

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", "資料訓練大表_v1.1.csv"))

class GeoRepository:
    @staticmethod
    def get_city_list() -> list[str]:
        data = pd.read_csv(file_path)
        return data["縣市"].unique().tolist()

    @staticmethod
    def get_district_list(city: str) -> list[str]:
        data = pd.read_csv(file_path)
        return data[data["縣市"] == city]["行政區"].unique().tolist()
    
    @staticmethod
    def get_neighborhood_list(city: str, district: str) -> list[str]:
        data = pd.read_csv(file_path)
        return data[(data["縣市"] == city) & (data["行政區"] == district)]["里別"].unique().tolist()
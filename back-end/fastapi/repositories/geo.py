import pandas as pd
import os
from common import REPORT_TABLE_FILE_NAME

report_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{REPORT_TABLE_FILE_NAME}"))

class GeoRepository:
    @staticmethod
    def get_city_list() -> list[str]:
        data = pd.read_csv(report_table_file_path)
        return data["縣市"].unique().tolist()

    @staticmethod
    def get_district_list(city: str) -> list[str]:
        data = pd.read_csv(report_table_file_path)
        return data[data["縣市"] == city]["行政區"].unique().tolist()
    
    @staticmethod
    def get_neighborhood_list(city: str, district: str) -> list[str]:
        data = pd.read_csv(report_table_file_path)
        return data[(data["縣市"] == city) & (data["行政區"] == district)]["里別"].unique().tolist()
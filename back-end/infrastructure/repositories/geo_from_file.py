import pandas as pd
import os
from common.constants import REPORT_TABLE_FILE_NAME
from domain.repositories.geo import IGeoRepository

report_table_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "datas", f"{REPORT_TABLE_FILE_NAME}"))

class GeoRepository(IGeoRepository):
    def __init__(self):
        self.data = pd.read_csv(report_table_file_path)

    def get_city_list(self) -> list[str]:
        return self.data["縣市"].unique().tolist()

    def get_district_list(self, city: str) -> list[str]:
        return self.data[self.data["縣市"] == city]["行政區"].unique().tolist()
    
    def get_neighborhood_list(self, city: str, district: str) -> list[str]:
        return self.data[(self.data["縣市"] == city) & (self.data["行政區"] == district)]["里別"].unique().tolist()
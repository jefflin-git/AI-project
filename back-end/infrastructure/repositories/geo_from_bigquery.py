from domain.repositories.geo import IGeoRepository
from common.constants import GCP_PROJECT_ID
from infrastructure.repositories.bigquery import BigQueryRepository

class GeoRepository(BigQueryRepository, IGeoRepository):
    def get_city_list(self) -> list[str]:
        query=f"""
        SELECT DISTINCT `縣市` FROM `{GCP_PROJECT_ID}.ai_project.prediction_data` ORDER BY `縣市` ASC;
        """
        return self._fetch_column_as_list(query, "縣市")

    def get_district_list(self, city: str) -> list[str]:
        query=f"""
        SELECT DISTINCT `行政區` FROM `{GCP_PROJECT_ID}.ai_project.prediction_data` WHERE `縣市` = '{city}' ORDER BY `行政區` ASC;
        """
        return self._fetch_column_as_list(query, "行政區")
    
    def get_neighborhood_list(self, city: str, district: str) -> list[str]:
        query=f"""
        SELECT DISTINCT `里別` FROM `{GCP_PROJECT_ID}.ai_project.prediction_data` WHERE `縣市` = '{city}' AND `行政區` = '{district}' ORDER BY `里別` ASC;
        """
        return self._fetch_column_as_list(query, "里別")
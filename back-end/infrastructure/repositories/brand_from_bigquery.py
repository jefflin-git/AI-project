from domain.repositories.brand import IBrandRepository
from common.constants import GCP_PROJECT_ID
from infrastructure.repositories.bigquery import BigQueryRepository

class BrandRepository(BigQueryRepository, IBrandRepository):
    def get_brand_list(self) -> list[str]:
        query=f"""
        SELECT brand FROM `{GCP_PROJECT_ID}.ai_project.brands`;
        """
        return self._fetch_column_as_list(query, "brand")
from domain.repositories.brand import IBrandRepository
from common.constants import GCP_PROJECT_ID
from infrastructure.repositories.bigquery import BigQueryRepository
from infrastructure.cache.redis import redis_cache

class BrandRepository(BigQueryRepository, IBrandRepository):
    @redis_cache(key_prefix='brands', ttl=86400)
    def get_brand_list(self) -> list[str]:
        query=f"""
        SELECT brand FROM `{GCP_PROJECT_ID}.ai_project.brands` ORDER BY brand ASC;
        """
        return self._fetch_column_as_list(query, "brand")
from google.cloud import storage, bigquery
import redis
from common.constants import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from log import Logger

logger = Logger(__name__)

class ClientManager:
    """集中管理客戶端連線"""
    def __init__(self):
        self._storage_client: storage.Client = None
        self._bigquery_client: bigquery.Client = None
        self.redis_conn: redis.Redis = None

    def init_clients(self):
        # 實際連線邏輯，可在 FastAPI lifespan 中呼叫
        try:
            self._storage_client = storage.Client()
            if not self._storage_client:
                raise RuntimeError("Storage client not initialized")
            logger.info("✅ Storage Client initialized.")
        except Exception as e:
            logger.error(f"❌ 建立 Storage Client 時發生錯誤: {e}")
            raise e

        try:
            self._bigquery_client = bigquery.Client()
            if not self._bigquery_client:
                raise RuntimeError("BigQuery client not initialized")
            logger.info("✅ BigQuery Client initialized.")
        except Exception as e:
            logger.error(f"❌ 建立 BigQuery Client 時發生錯誤: {e}")
            raise e
        
        try:
            pool = redis.ConnectionPool(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                password=REDIS_PASSWORD,
                decode_responses=True, # 自動將 bytes 轉為 str
                socket_timeout=2.0
            )
            self._redis_conn = redis.Redis(connection_pool=pool)
            if not self._redis_conn:
                raise RuntimeError("Redis Client 未初始化")
            logger.info("✅ Redis Client initialized.")
        except Exception as e:
            logger.error(f"❌ 建立 Redis Client 時發生錯誤: {e}")
            raise e
    
    def close_clients(self):
        try:
            if self._storage_client:
                self._storage_client.close()
                logger.info("Storage client closed.")
                self._storage_client = None
            if self._bigquery_client:
                self._bigquery_client.close()
                logger.info("BigQuery client closed.")
                self._bigquery_client = None
            if self._redis_conn:
                self._redis_conn.close()
                logger.info("Redis client closed.")
                self._redis_conn = None
        except Exception as e:
            logger.warning(f"⚠️ 關閉時發生錯誤（忽略）: {str(e)}")
            raise e

    @property
    def storage(self) -> storage.Client:
        return self._storage_client

    @property
    def bigquery(self) -> bigquery.Client:
        return self._bigquery_client

    @property
    def redis(self) -> redis.Redis:
        return self._redis_conn

# 建立一個全域實例供 Lifespan 使用
client_manager = ClientManager()
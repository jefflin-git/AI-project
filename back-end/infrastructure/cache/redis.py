from functools import wraps
import json
from infrastructure.client import client_manager
from log import Logger

logger = Logger(__name__)

def redis_cache(key_prefix: str, ttl: int = 3600):
    """
    Redis 快取裝飾器
    :param key_prefix: 快取鍵的前綴 (例如 'geo:districts')
    :param ttl: 快取存活時間 (秒)，預設 1 小時
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args):
            # 1. 組合唯一的 Cache Key
            # 將參數轉為字串並拼接，例如 'geo:districts:Taipei:Xinyi'
            logger.debug(f"Args: {args}")
            arg_str = ":".join([str(arg) for arg in args])
            cache_key = f"{key_prefix}:{arg_str}".strip(":")
            logger.debug(f"Cache Key: {cache_key}")

            try:
                # 2. 嘗試從 Redis 讀取
                cached_val = client_manager.redis.get(cache_key)
                if cached_val:
                    logger.debug(f"Cache Hit: {cache_key}, value: {cached_val}")
                    return json.loads(cached_val)
            except Exception as e:
                # 如果 Redis 壞了，記錄錯誤但繼續執行原始函式 (Fail-safe)
                logger.error(f"Redis Error (Read): {e}")

            # 3. 執行原始的資料庫查詢 (例如 BigQuery)
            result = func(self, *args)
            logger.debug(f"Result: {result}")

            try:
                # 4. 寫入 Redis
                if result is not None:
                    val_str = json.dumps(result, ensure_ascii=False)
                    client_manager.redis.setex(
                        name=cache_key,
                        time=ttl,
                        value=val_str
                    )
                    logger.debug(f"Cache Set: {cache_key}, value: {val_str}")
            except Exception as e:
                logger.error(f"Redis Error (Write): {e}")

            return result
        return wrapper
    return decorator
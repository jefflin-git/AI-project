from google.cloud import storage
from log import Logger

logger = Logger(__name__)

class GCSRepository:
    @staticmethod
    def get_gcs_file(bucket_name: str, file_name: str, local_file_path: str):
        try:
            # """從 GCS 下載模型檔"""
            logger.info(f"正在從 gs://{bucket_name}/{file_name} 下載模型...")
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(file_name)
            blob.download_to_filename(local_file_path)
            logger.info("下載完成！")
        except Exception as e:
            logger.error(f"❌ 資源下載失敗: {str(e)}")
            raise e
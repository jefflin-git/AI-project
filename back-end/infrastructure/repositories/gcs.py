from google.cloud import storage
from infrastructure.client import client_manager
from log import Logger
from domain.repositories.storage import IStorageRepository

logger = Logger(__name__)

class GCSRepository(IStorageRepository):
    def __init__(self):
        self.storage_client: storage.Client = client_manager.storage
        
    def download_file(self, folder_name: str, file_name: str, local_file_path: str):
        try:
            logger.info(f"正在從 gs://{folder_name}/{file_name} 下載檔案...")
            bucket = self.storage_client.bucket(folder_name)
            blob = bucket.blob(file_name)
            blob.download_to_filename(local_file_path)
            logger.info("下載完成！")
        except Exception as e:
            logger.error(f"❌ 資源下載失敗: {str(e)}")
            raise e
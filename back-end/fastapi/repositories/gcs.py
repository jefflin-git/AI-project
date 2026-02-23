from google.cloud import storage

class GCSRepository:
    @staticmethod
    def get_gcs_file(bucket_name: str, file_name: str, local_file_path: str) -> bytes:
        # """從 GCS 下載模型檔"""
        print(f"正在從 gs://{bucket_name}/{file_name} 下載模型...")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_file_path)
        print("下載完成！")
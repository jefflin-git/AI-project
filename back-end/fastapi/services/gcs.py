from repositories.gcs import GCSRepository

class GCSService:
    @staticmethod
    def get_gcs_file(bucket_name: str, file_name: str, local_file_path: str) -> bytes:
        return GCSRepository.get_gcs_file(bucket_name, file_name, local_file_path)
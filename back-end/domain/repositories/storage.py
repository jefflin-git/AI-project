from abc import ABC, abstractmethod

class IStorageRepository(ABC):
    @abstractmethod
    def download_file(self, folder_name: str, file_name: str, local_file_path: str):
        pass
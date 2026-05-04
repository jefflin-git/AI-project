from abc import ABC, abstractmethod

class IBrandRepository(ABC):
    @abstractmethod
    def get_brand_list(self) -> list[str]:
        pass
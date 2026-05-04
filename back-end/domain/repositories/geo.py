from abc import ABC, abstractmethod

class IGeoRepository(ABC):
    @abstractmethod
    def get_city_list(self) -> list[str]:
        pass

    @abstractmethod
    def get_district_list(self, city: str) -> list[str]:
        pass
    
    @abstractmethod
    def get_neighborhood_list(self, city: str, district: str) -> list[str]:
        pass
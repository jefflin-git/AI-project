from repositories.geo import GeoRepository

class GeoService:
    @staticmethod
    def get_city_list() -> list[str]:
        return GeoRepository.get_city_list()

    @staticmethod
    def get_district_list(city: str) -> list[str]:
        return GeoRepository.get_district_list(city)

    @staticmethod
    def get_neighborhood_list(city: str, district: str) -> list[str]:
        return GeoRepository.get_neighborhood_list(city, district)

    @staticmethod
    def check_valid_geo(city: str, district: str, neighborhood: str) -> bool:
        result = GeoRepository.get_neighborhood_list(city, district)
        return neighborhood in result
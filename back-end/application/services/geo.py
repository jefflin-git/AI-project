from domain.repositories.geo import IGeoRepository

class GeoService:
    def __init__(self, geo_repository: IGeoRepository):
        self.geo_repository = geo_repository

    def get_city_list(self) -> list[str]:
        return self.geo_repository.get_city_list()

    def get_district_list(self, city: str) -> list[str]:
        return self.geo_repository.get_district_list(city)

    def get_neighborhood_list(self, city: str, district: str) -> list[str]:
        return self.geo_repository.get_neighborhood_list(city, district)

    def check_valid_geo(self, city: str, district: str, neighborhood: str) -> bool:
        result = self.get_neighborhood_list(city, district)
        return neighborhood in result
from repositories.brand import BrandRepository

class BrandService:
    @staticmethod
    def get_brand_list() -> list[str]:
        return BrandRepository.get_brand_list()
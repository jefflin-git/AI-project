from domain.repositories.brand import IBrandRepository

class BrandService:
    def __init__(self, brand_repository: IBrandRepository):
        self.brand_repository = brand_repository

    def get_brand_list(self) -> list[str]:
        return self.brand_repository.get_brand_list()
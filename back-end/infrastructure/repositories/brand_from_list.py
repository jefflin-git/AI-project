from domain.repositories.brand import IBrandRepository

class BrandRepository(IBrandRepository):
    def get_brand_list(self) -> list[str]:
        return ["便利商店", "超市及藥妝"]
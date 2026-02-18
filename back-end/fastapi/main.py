from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.geo import GeoService
from services.brand import BrandService
from services.prediction import PredictionService
from repositories.prediction import PredictionRepository

app = FastAPI()
uri_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(uri_prefix + "/cities")
async def get_city_list():
    return GeoService.get_city_list()

@app.get(uri_prefix + "/districts/{city}")
async def get_district_list(city: str):
    return GeoService.get_district_list(city)

@app.get(uri_prefix + "/neighborhoods/{city}/{district}")
async def get_neighborhood_list(city: str, district: str):
    return GeoService.get_neighborhood_list(city, district)

@app.get(uri_prefix + "/brands")
async def get_brand_list():
    return BrandService.get_brand_list()

@app.get(uri_prefix + "/geo-check/{city}/{district}/{neighborhood}")
async def check_valid_geo(city: str, district: str, neighborhood: str):
    return {"is_valid": GeoService.check_valid_geo(city, district, neighborhood)}

@app.get(uri_prefix + "/run-prediction/{city}/{district}/{neighborhood}/{brand}")
async def run_prediction(city: str, district: str, neighborhood: str, brand: str):
    brand_type = 1 if brand == "便利商店" else 0
    prediction = PredictionService(PredictionRepository()).run_prediction(city, district, neighborhood, brand_type)
    return {
        "operation": {
            "score": prediction.operation.score,
            "report": prediction.operation.report,
        },
        "totalPopulation": {
            "neighborhood": prediction.total_population.neighborhood,
            "district": prediction.total_population.district,
        },
        "medianIncome": {
            "neighborhood": prediction.median_income.neighborhood,
            "district": prediction.median_income.district,
        },
        "competitorCount": prediction.competitor_count,
        "aiInsight": prediction.ai_insight,
        "radar": {
            "labels": prediction.radar.labels,
            "values": prediction.radar.values,
        },
        "isSuccess": prediction.is_success
    }


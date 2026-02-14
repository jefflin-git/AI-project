from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.geo import get_city_list, get_district_list, get_neighborhood_list
from services.brand import get_brands_list
from services.geo import is_valid_geo

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
async def get_cities():
    return get_city_list()

@app.get(uri_prefix + "/districts/{city}")
async def get_districts(city: str):
    return get_district_list(city)

@app.get(uri_prefix + "/neighborhoods/{city}/{district}")
async def get_neighborhoods(city: str, district: str):
    return get_neighborhood_list(city, district)

@app.get(uri_prefix + "/brands")
async def get_brands():
    return get_brands_list()

@app.get(uri_prefix + "/geo_check/{city}/{district}/{neighborhood}")
async def is_valid_geo(city: str, district: str, neighborhood: str):
    return is_valid_geo(city, district, neighborhood)

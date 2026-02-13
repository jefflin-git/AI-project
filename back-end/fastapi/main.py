from fastapi import FastAPI
from services.geo import get_city_list, get_district_list, get_neighborhood_list

app = FastAPI()
uri_prefix = "/api"

@app.get(uri_prefix + "/cities")
async def get_cities():
    return get_city_list()

@app.get(uri_prefix + "/districts/{city}")
async def get_districts(city: str):
    return get_district_list(city)

@app.get(uri_prefix + "/neighborhoods/{city}/{district}")
async def get_neighborhoods(city: str, district: str):
    return get_neighborhood_list(city, district)
from repositories.geo import get_city_list_from_csv, get_district_list_from_csv, get_neighborhood_list_from_csv


def get_city_list():
    return get_city_list_from_csv()

def get_district_list(city):
    return get_district_list_from_csv(city)

def get_neighborhood_list(city, district):
    return get_neighborhood_list_from_csv(city, district)

def is_valid_geo(city, district, neighborhood):
    return city in get_city_list() and district in get_district_list(city) and neighborhood in get_neighborhood_list(city, district)
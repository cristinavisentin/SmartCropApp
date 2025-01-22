import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
from datetime import datetime
# Thanks to https://open-meteo.com/en/docs/historical-weather-api for the data

def get_climate_data(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    start_date = f"{datetime.now().year-1}-01-01"
    end_date = f"{datetime.now().year-1}-12-31"

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()
    temperature_max = daily.Variables(0).ValuesAsNumpy()
    temperature_min = daily.Variables(1).ValuesAsNumpy()
    precipitation_sum = daily.Variables(2).ValuesAsNumpy()

    avg_temperature = ((temperature_max + temperature_min) / 2).mean()
    avg_rainfall = precipitation_sum.sum()
    return avg_temperature, avg_rainfall


def get_country_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location and "country" in location.raw["address"]:
        return location.raw["address"]["country"]
    else:
        raise ValueError("Unable to determine the country from the provided coordinates.")

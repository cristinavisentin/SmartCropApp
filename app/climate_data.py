import openmeteo_requests
import requests_cache
import numpy as np
from retry_requests import retry
from datetime import datetime
# Thanks to https://open-meteo.com/en/docs/historical-weather-api for the data

def calculate_annual_avg_temperature(temp_max, temp_min):
    daily_avg = (temp_max + temp_min) / 2
    return round(np.mean(daily_avg), 1)


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
    daily_avg = (temperature_max + temperature_min) / 2
    avg_yearly_temperature = round(np.mean(daily_avg), 1)

    precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    precipitation_sum = float(precipitation_sum.sum())
    precipitation_sum = int(round(precipitation_sum))

    return avg_yearly_temperature, precipitation_sum

# weather.py
import requests
from config.config import API_KEY, CITY
from datetime import datetime

#gets todays weather
def get_weather():
    #pull api for weather
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=imperial&appid={API_KEY}'
    response = requests.get(url).json()

    #tries to pull data from the API
    try:
        #temp
        temp = response['main']['temp']
        #weather description
        desc = response['weather'][0]['description'].capitalize()
        #grabs weather icon
        icon_code = response['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        #returns temp and icon with description
        return f"{temp:.1f}°F - {desc}", icon_url
    #api failure case
    except KeyError:
        return "Weather unavailable", None


def get_forecast():
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=imperial&appid={API_KEY}'
    response = requests.get(url).json()
    
    #creates list for forecast
    forecasts = []
    seen_dates = set()

    try:
        for entry in response['list']:
            dt_txt = entry['dt_txt']
            date_str, time_str = dt_txt.split()

            if time_str == "12:00:00" and date_str not in seen_dates:
                seen_dates.add(date_str)

                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                weekday = date_obj.strftime('%A')

                temp = entry['main']['temp']
                desc = entry['weather'][0]['description'].capitalize()
                icon_code = entry['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

                forecasts.append((f"{weekday}: {temp:.0f}°F, {desc}", icon_url))

            if len(forecasts) >= 3:
                break
    except KeyError:
        forecasts = [("Forecast unavailable", None)]

    return forecasts

# weather.py
import requests
from config import API_KEY, CITY

def get_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=imperial&appid={API_KEY}'
    response = requests.get(url).json()

    try:
        temp = response['main']['temp']
        desc = response['weather'][0]['description'].capitalize()
        icon_code = response['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        return f"{temp:.1f}°F - {desc}", icon_url
    except KeyError:
        return "Weather unavailable"
import json
import requests
import key_manager 
key_path = key_manager.get_keypath("openweather")
with open(key_path, 'r') as f:
    key = f.read().strip()
#print(key)
nylat = "40.717831142775566" 
nylon = "-74.0137791697529"
endpoint = "https://api.openweathermap.org/data/2.5/weather"
# response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={nylat}&lon={nylon}&appid={key}")
#print(json.loads(response.text))
def kelvin_to_fahrenheit(temp):
    F = 1.8*(temp-273) + 32
    return F
def get_weather_data(lat=nylat, lon=nylon):
    response = requests.get(f"{endpoint}?lat={nylat}&lon={nylon}&appid={key}")
    weather_info = json.loads(response.text)
    icon = weather_info['weather'][0]['icon']
    iconUrl = f"https://openweathermap.org/img/wn/{icon}@2x.png"
    temp_min = round(kelvin_to_fahrenheit(weather_info["main"]["temp_min"]), 1)
    temp_max = round(kelvin_to_fahrenheit(weather_info["main"]["temp_max"]), 1)
    return {'low': temp_min,
            'high': temp_max,
            'img_url':iconUrl,
            'type': weather_info["main"],
            'temp': weather_info["main"]["temp"],
            'feels_like': weather_info["main"]["feels_like"],
            'name': weather_info["name"]}
#print(getweatherdata())
# response = requests.get(endpoint,
# {"appid": key,
#  "lat": nylat,
#  "lon": nylon,
#  "unis": "imperial"})

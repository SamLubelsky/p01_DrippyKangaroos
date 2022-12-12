import json
import requests
with open('keys/key_openweather.txt', 'r') as f:
    key = f.read().strip()
    key = "361f1468f4f95c0aff4c25ae9e3c7b3d"
print(key)
nylat = "40.717831142775566" 
nylon = "-74.0137791697529"
endpoint = "https://api.openweathermap.org/data/2.5/weather"
response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={nylat}&lon={nylon}&appid={key}")
# response = requests.get(endpoint,
# {"appid": key,
#  "lat": nylat,
#  "lon": nylon,
#  "unis": "imperial"})
print(response.text)

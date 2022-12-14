import requests

startpoint = "https://data.alpaca.markets/v2/stocks"
API_KEY_ID = ""
SECRET_KEY = ""
with open("keys/key_newsapi.txt", 'r') as k:
    k = k.read().strip().splitlines()
    API_KEY_ID = k[0]
    SECRET_KEY = k[1]

headers = {
    "APCA-API-KEY-ID": API_KEY_ID,
    "APCA-API-SECRET-KEY": SECRET_KEY,
}

def request_stock(stock):
    url = f"{startpoint}/{symbol}/quotes/latest"
    response = requests.get(url, headers=headers)
    return response.json()
from urllib.request import urlopen
import json

startpoint = "https://paper-api.alpaca.markets/"
api_key = ""
with open("keys/key_newsapi.txt", 'r') as k:
    api_key = k.read().strip() 
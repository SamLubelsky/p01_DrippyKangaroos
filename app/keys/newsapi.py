from urllib.request import urlopen
import json

endpoint = "https://newsapi.org/v2/everything?"
api_key = ""
with open("key_newsapi.txt", 'r') as k:
    api_key = k.read().strip() 

def request(query):
    url = f"{endpoint}q={query}&apiKey={api_key}}"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json

if __name__ == "__main__":
    print(request("bitcoin"))


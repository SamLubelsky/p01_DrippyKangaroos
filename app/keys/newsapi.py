from urllib.request import urlopen
import json

endpoint = "https://newsapi.org/v2/everything?"
api_key = ""
with open("key_newsapi.txt", 'r') as k:
    api_key = k.read().strip() 

def request(title):
    url = f"{endpoint}q={title}&apiKey={api_key}"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json["articles"]



if __name__ == "__main__":
    articles = request("bitcoin")
    for article in articles:
        print(article["title"])
        print(article["url"])
        #print(article["summary"])
    #print(articles)



from urllib.request import urlopen
import json

endpoint = "https://newsapi.org/v2/everything?"
api_key = ""
with open("key_newsapi.txt", 'r') as k:
    api_key = k.read().strip() 

def request_articles(query, n=1):
    url = f"{endpoint}q={query}&language=en&apiKey={api_key}"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json["articles"][:n]

def article_info(article):
    return {
            "url": article["url"],
            "image": article["urlToImage"],
            "title": article["title"], 
            "description": article["description"],
            "date": article["publishedAt"][:10],
            "author": article["author"]
        }

if __name__ == "__main__":
    articles = request_articles("bitcoin", 3)
    for article in articles:
        info = article_info(article)
        print(info)



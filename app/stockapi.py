from urllib.request import urlopen
import json
# https://syncwith.com/yahoo-finance/yahoo-finance-api
startpoint = "https://query1.finance.yahoo.com/v11/finance/quoteSummary"

api_key = ""
with open("keys/key_newsapi.txt", 'r') as k:
    api_key = k.read().strip().splitlines()


def request_stock(stock):
    url = f"{startpoint}/{stock}?modules=financialData"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json["quoteSummary"]["result"][0]["financialData"]


def get_price(stock):
    stock = request_stock(stock)
    return stock["currentPrice"]["fmt"]
print(get_price("aapl"))

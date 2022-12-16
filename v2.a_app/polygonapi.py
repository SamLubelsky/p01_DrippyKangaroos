import requests
import json
from datetime import date, timedelta
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse


key = ""
with open("keys/key_polygon.txt", 'r') as k:
    key = k.read().strip() 
#https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=*


todate = date.today()
yestdate = todate - timedelta(days = 1)
c = RESTClient(key)

def request_stock_agg(stock):
    agg_url = cast(HTTPResponse,c.get_aggs(stock, 1, "day", yestdate, todate, raw=True,),)
    #url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{yestdate}/{todate}"
    return agg_url.data

print(request_stock_agg("AAPL"))

def stocks():
    #top = cast(HTTPResponse,c.get_snapshot_all("stocks"),)
    #top 20s
    gainers = cast(HTTPResponse,c.get_snapshot_all("stocks", "gainers",),)
    losers = cast(HTTPResponse,c.get_snapshot_all("stocks", "losers",),)
    #s.data[tickers][ticker]
    #https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey=*

stocks()
#Resources/Docs Used (for further reference)
#https://github.com/polygon-io/client-python
#https://polygon.io/docs/stocks/getting-started
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
    agg = cast(HTTPResponse,c.get_aggs(stock, 1, "day", yestdate, todate, raw=True,),)
    #url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{yestdate}/{todate}"
    return agg.data

print(request_stock_agg("AAPL"))

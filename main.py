from iexfinance.stocks import Stock
import pandas as pd
import http.client
import json

# get latest price when given ticker
def getLatestPrice(ticker):
    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
    connection = http.client.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
    # Headers
    headers = {"Accept":"application/json",
            "Authorization":"Bearer A5dHAZqYNutmBOjIzppnWIsAwYw4"}
    # Send synchronously
    connection.request('GET', '/v1/markets/quotes?symbols={}'.format(ticker), None, headers)
    try:
        response = connection.getresponse()
        content = response.read()
        # Success
        return json.loads(content)["quotes"]["quote"]["last"]
    except http.client.HTTPException as e:
        # Exception
        print('Exception during request')

print(getLatestPrice("AAPL"))
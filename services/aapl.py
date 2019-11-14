import pandas as pd
import http.client
import json
import MySQLdb

# Config values
ticker="AAPL"
key = "A5dHAZqYNutmBOjIzppnWIsAwYw4"
db_host = "35.237.245.229"
db_user = "root"
db_password = "cis4930"

# Connects to database
try:
    db = MySQLdb.connect(host=db_host,user=db_user,password=db_password)
except:
    print("Could not connect to aapl database, is it up?")

# get latest price when given ticker using tradier's example code
def getLatestPrice(key=key, ticker=ticker):
    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
    connection = http.client.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
    # Headers
    headers = {"Accept":"application/json", "Authorization":"Bearer "+key}
    # Send synchronously
    connection.request('GET', '/v1/markets/quotes?symbols={}'.format(ticker), None, headers)
    try:
        response = connection.getresponse()
        content = response.read()
        # Success
        return json.loads(content)["quotes"]["quote"]["last"]
    except http.client.HTTPException:
        # Exception
        print('Exception during request')

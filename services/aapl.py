import pandas as pd
import http.client
import json
import MySQLdb

key = "A5dHAZqYNutmBOjIzppnWIsAwYw4"
db_host = "35.237.245.229"
db_user = "root"
db_password = "admin"

# get latest price when given ticker using tradier's example code
def getLatestPrice(key, ticker="AAPL"):
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
    except http.client.HTTPException as e:
        # Exception
        print('Exception during request')

db = MySQLdb.connect(host=db_host,user=db_user,password=db_password)

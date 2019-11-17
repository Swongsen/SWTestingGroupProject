import pandas as pd
import http.client
import json
from flask import jsonify
from services import connect, monitoring
#import connect

# Config values
ticker="aapl"
tradier_key = "A5dHAZqYNutmBOjIzppnWIsAwYw4"

cur = connect.cursor
# get latest price when given ticker using tradier's example code
def getLatestPrice(key, tradier_key=tradier_key, ticker=ticker.upper()):
    key = int(key)
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountid={}".format(key))
    result = cur.fetchone()
    if result == None:
        return "Invalid API key"

    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
    connection = http.client.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
    # Headers
    headers = {"Accept":"application/json", "Authorization":"Bearer "+tradier_key}
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

def buy(amount, key):
    key = int(key)
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountid={}".format(key))
    result = cur.fetchone()
    if result == None:
        return "Invalid API key"

    # log transaction
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
    cur.execute("USE {}".format(ticker))
    price = getLatestPrice(key)
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("INSERT INTO transactions(accountid, type, amount, price, created_at) VALUES ({}, 'buy', {}, {}, NOW())".format(key, amount, price))

    #update accounts database
    cur.execute("USE accounts")
    cur.execute("SELECT funds, {} FROM accounts WHERE accountid = {}".format(ticker, key))
    results = cur.fetchone()

    #subtract funds from account, add stocks to account
    total_funds = float(results[0])
    total_stocks = int(results[1])
    funds_left = total_funds - (price * float(amount))
    stocks_added = total_stocks + float(amount)
    cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, key))  
    return "Successfully bought {} stocks of {}".format(amount, ticker)

def sell(amount, key):
    key = int(key)
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountid={}".format(key))
    result = cur.fetchone()
    if result == None:
        return "Invalid API key"

    # log transaction
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
    cur.execute("USE {}".format(ticker))
    price = getLatestPrice(key)
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("INSERT INTO transactions(accountid, type, amount, price, created_at) VALUES ({}, 'buy', {}, {}, NOW())".format(key, amount, price))

    #update accounts database
    cur.execute("USE accounts")
    cur.execute("SELECT funds, {} FROM accounts WHERE accountid = {}".format(ticker, key))
    results = cur.fetchone()

    #subtract funds from account, add stocks to account
    total_funds = float(results[0])
    total_stocks = int(results[1])
    funds_left = total_funds + (price * float(amount))
    stocks_added = total_stocks - float(amount)
    cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, key))
    return "Successfully bought {} stocks of {}".format(amount, ticker)


getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "aapl")

import pandas as pd
import http.client
import json
from flask import jsonify
from services import connect, monitoring
#import connect

# Config values
ticker="amzn"
tradier_key = "A5dHAZqYNutmBOjIzppnWIsAwYw4"

cur = connect.cursor
cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
cur.execute("CREATE DATABASE IF NOT EXISTS accounts")
cur.execute("CREATE TABLE IF NOT EXISTS accounts(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, accountname TEXT NOT NULL, funds DOUBLE NOT NULL, aapl INTEGER NOT NULL, fb INTEGER NOT NULL, nflx INTEGER NOT NULL, amzn INTEGER NOT NULL, created_at TEXT NOT NULL)")
cur.execute("USE {}".format(ticker))
cur.execute("CREATE TABLE IF NOT EXISTS transactions(userid INTEGER, accountid INTEGER, type TEXT, amount INTEGER, price DOUBLE, created_at TEXT NOT NULL)")
    
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

def trade(trade_type, amount, key):
    amount = int(amount)
    key = int(key)
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountid={}".format(key))
    result = cur.fetchone()
    if result == None:
        return "Invalid API key"

    # log transaction
    price = getLatestPrice(key)
    monitoring.log("stocktransaction", (ticker, "NULL", key, trade_type, amount, price))

    #update accounts database
    cur.execute("USE accounts")
    cur.execute("SELECT funds, {} FROM accounts WHERE accountid = {}".format(ticker, key))
    results = cur.fetchone()

    #subtract funds from account, add stocks to account
    total_funds = float(results[0])
    total_stocks = int(results[1])

    #check bank account
    cur.execute("SELECT {}, funds FROM accounts WHERE accountid=0".format(ticker))
    results = cur.fetchone()
    bank_stock = results[0]
    bank_funds = results[1]

    # buy more if not enough
    if int(bank_stock) < amount and key != 0 and trade_type=="buy":
        bank_stock = bank_stock + amount
        cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid=0".format(bank_funds-price*float(amount), ticker, bank_stock+amount))
    
    # update bank and client
    if trade_type == "buy":
        funds_left = total_funds - (price * float(amount))
        if funds_left < 0:
            return "Not enough funds"
        stocks_added = total_stocks + float(amount)
        cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, key))  
        if key!=0:
            cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid=0".format(bank_funds+price*float(amount), ticker, bank_stock-amount))
        return "Successfully bought {} stocks of {}".format(amount, ticker)
    
    elif trade_type == "sell":
        funds_left = total_funds + (price * float(amount))
        stocks_added = total_stocks - float(amount)
        if stocks_added < 0:
            return "Not enough stocks"
        cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, key))  
        if key!=0:
            cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid=0".format(bank_funds-price*float(amount), ticker, bank_stock+amount))
        return "Successfully sold {} stocks of {}".format(amount, ticker)

def buy(amount, key):
    trade("buy", amount, key)

def sell(amount, key):
    trade("sell", amount, key)

getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", ticker)

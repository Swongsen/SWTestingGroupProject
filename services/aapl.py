import pandas as pd
import http.client
import json
import connect

# Config values
ticker="aapl"
key = "A5dHAZqYNutmBOjIzppnWIsAwYw4"

cur = connect.cursor
# get latest price when given ticker using tradier's example code
def getLatestPrice(key=key, ticker=ticker.upper()):
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

def buy(session, amount):
    # get accountid from accountname and userid
    accountname = session["token"]
    userid = session["userid"]
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountname = '{}' AND userid = {}".format(accountname, userid))
    account = cur.fetchone()[0]

    # log transaction
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
    cur.execute("USE {}".format(ticker))
    price = getLatestPrice()
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("INSERT INTO transactions(accountid, type, amount, price, created_at) VALUES ({}, 'buy', {}, {}, NOW())".format(account, amount, price))

    #update accounts database
    cur.execute("USE accounts")
    cur.execute("SELECT funds, {} FROM accounts WHERE accountid = {}".format(ticker, account))
    results = cur.fetchone()

    #subtract funds from account, add stocks to account
    total_funds = float(results[0])
    total_stocks = int(results[1])
    funds_left = total_funds - (price * float(amount))
    stocks_added = total_stocks + float(amount)
    print("UPDATE accounts SET funds = {} AND {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, account))
    cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, account))
    return "Successfully bought {} stocks of {}".format(amount, ticker)

def sell(session, amount):
    # get accountid from accountname and userid
    accountname = session["token"]
    userid = session["userid"]
    cur.execute("USE accounts")
    cur.execute("SELECT accountid FROM accounts WHERE accountname = '{}' AND userid = {}".format(accountname, userid))
    account = cur.fetchone()[0]

    # log transaction
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
    cur.execute("USE {}".format(ticker))
    price = getLatestPrice()
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("INSERT INTO transactions(accountid, type, amount, price, created_at) VALUES ({}, 'buy', {}, {}, NOW())".format(account, amount, price))

    #update accounts database
    cur.execute("USE accounts")
    cur.execute("SELECT funds, {} FROM accounts WHERE accountid = {}".format(ticker, account))
    results = cur.fetchone()

    #subtract funds from account, add stocks to account
    total_funds = float(results[0])
    total_stocks = int(results[1])
    funds_left = total_funds + (price * float(amount))
    stocks_added = total_stocks - float(amount)
    print("UPDATE accounts SET funds = {} AND {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, account))
    cur.execute("UPDATE accounts SET funds = {}, {} = {} WHERE accountid = {}".format(funds_left, ticker, stocks_added, account))
    return "Successfully bought {} stocks of {}".format(amount, ticker)

getLatestPrice()

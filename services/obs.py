import pandas as pd
from flask import jsonify
from services import connect

cur = connect.cursor
cur.execute("CREATE DATABASE IF NOT EXISTS accounts")
cur.execute("USE accounts")

""" ACCOUNT MANAGEMENT """
# Add an account with starting $ for a user
def addAccount(userID, accountname, starting_balance):
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, accountname TEXT NOT NULL, funds DOUBLE NOT NULL, aapl INTEGER NOT NULL, fb INTEGER NOT NULL, nflx INTEGER NOT NULL, amzn INTEGER NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT COUNT(*) FROM accounts")
    num_accounts = cur.fetchone()[0]
    cur.execute("INSERT INTO accounts(userid, accountid, accountname, funds, aapl, fb, nflx, amzn, created_at) VALUES ({},{},'{}',{},0,0,0,0,NOW())".format(userID,num_accounts,accountname,starting_balance))
    return 1

# View balance for a given account
def viewAccountBalance(account):
    return 1

""" TRANSACTIONS """
# Add money to a given account
def addFunds(account):
    return 1

# Buy an amount of shares of a certain ticker for an account
def buyShare(account, ticker, amount):
    return 1

# Sell an amount of shares of a certain ticker for an account
def sellShare(account, ticker, amount):
    return 1

""" NET WORTH """
# Get total account balances and shares owned
def netWorth(user):
    return 1

""" DEBUG """
def viewAccounts():
    cur.execute("CREATE DATABASE IF NOT EXISTS accounts")
    cur.execute("USE accounts")
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, accountname TEXT NOT NULL, funds DOUBLE NOT NULL, aapl INTEGER NOT NULL, fb INTEGER NOT NULL, nflx INTEGER NOT NULL, amzn INTEGER NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM accounts")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

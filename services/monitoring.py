import pandas as pd
from flask import jsonify
from services import connect

cur = connect.cursor
cur.execute("CREATE DATABASE IF NOT EXISTS logs")
cur.execute("USE logs")
cur.execute("DROP TABLE transactions")
cur.execute("CREATE TABLE IF NOT EXISTS transactions(userid INTEGER, accountid INTEGER, type TEXT, amount INTEGER, price DOUBLE, created_at TEXT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS authentication(userid INTEGER NOT NULL, username TEXT NOT NULL, created_at TEXT NOT NULL)")
        

# log function that should be able to log anything
# type should be either: 
# authentication, transaction, or stock transaction
def log(table, information):
    # information format = (userid, username)
    if table == "authentication":
        cur.execute("USE logs")
        cur.execute("INSERT INTO authentication(userid, username, created_at) VALUES ({},'{}',NOW())".format(information[0],information[1]))
    # information format = (userid, accountid, type, amount, price)
    elif table == "transaction":
        cur.execute("USE logs")
        cur.execute("INSERT INTO transactions(userid, accountid, type, amount, price, created_at) VALUES ({},{},'{}',{},{},NOW())".format(information[0],information[1],information[2],information[3],information[4]))
    # information format = (ticker, userid, accountid, type, amount, price)
    elif table == "stocktransaction":
        # log in all transactions
        cur.execute("USE logs")
        cur.execute("INSERT INTO transactions(userid, accountid, type, amount, price, created_at) VALUES ({},{},'{}',{},{},NOW())".format(information[0],information[1],information[2],information[3],information[4],information[5]))


# ADMIN VIEW OF LOGS
# No login required
def viewAuthenticationLogs():
    cur.execute("USE logs")
    cur.execute("CREATE TABLE IF NOT EXISTS authentication(userid INTEGER NOT NULL, username TEXT NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM authentication")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

def viewTransactionLogs():
    cur.execute("USE logs")
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM transactions")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

def viewStockTransactionLogs(ticker):
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(ticker))
    cur.execute("USE {}".format(ticker))
    cur.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, type TEXT NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM transactions")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
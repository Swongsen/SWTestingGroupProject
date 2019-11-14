import pandas as pd
from flask import jsonify
from services import connect

cur = connect.cursor
cur.execute("CREATE DATABASE IF NOT EXISTS logs")
cur.execute("USE logs")

# log function that should be able to log anything
# type should be either: 
# authentication, transaction, or stock transaction
def log(table, information):
    if table == "authentication":
        cur.execute("CREATE TABLE IF NOT EXISTS authentication(userid INTEGER NOT NULL, username TEXT NOT NULL, created_at TEXT NOT NULL)")
        cur.execute("INSERT INTO authentication(userid, username, created_at) VALUES ({},'{}',NOW())".format(information[0],information[1]))
    elif table == "transaction":
        return 1
    elif table == "stocktransaction":
        return 1
    return 1

# ADMIN VIEW OF LOGS
# No login required
def viewAuthenticationLogs():
    cur.execute("CREATE TABLE IF NOT EXISTS authentication(userid INTEGER NOT NULL, username TEXT NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM authentication")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

def viewTransactionLogs():
    return 1

def viewStockTransactionLogs():
    return 1
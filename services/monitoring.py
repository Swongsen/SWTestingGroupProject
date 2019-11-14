import pandas as pd
import MySQLdb
from flask import jsonify

# Config values
db_host = "34.73.169.74"
db_user = "root"
db_password = "cis4930"

# Connects to database, set up cursor
try:
    db = MySQLdb.connect(host=db_host,user=db_user,password=db_password)
except:
    print("Could not connect to OBS database, is it up?")
cur = db.cursor()
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
    elif table == "stock transaction":
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

def viewStockTransactions():
    return 1
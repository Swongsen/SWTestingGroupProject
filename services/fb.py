import mysql.connector
from main import getLatestPrice
from datetime import datetime
import json

facebookdb = mysql.connector.connect(host="remotemysql.com", port=3306, user="EIsUYT2e02", passwd="pxpKuKcuE9", database="EIsUYT2e02")
facebookcursor = facebookdb.cursor(buffered=True)

facebookcursor.execute("CREATE TABLE IF NOT EXISTS fb_user_stocks \
                        (username VARCHAR(255), number_stocks INT, total_amount DOUBLE)") # stores each user's number of FB stocks and total value of them
facebookcursor.execute("CREATE TABLE IF NOT EXISTS fb_user_trnsctns \
                    (date VARCHAR(255), username VARCHAR(255), number_stocks INT, total_amount DOUBLE)") # stores every transaction of every user


def modify_user_stocks(user, number_of_stocks): # method used to buy/sell shares, use negative number for number_of_stocks when selling
    sql = "SELECT * FROM fb_user_stocks WHERE username = %s"
    value = (user, )
    facebookcursor.execute(sql, value)
    result = facebookcursor.fetchall()

    if len(result) == 0: # if user doesn't exist in database
        sql = "INSERT INTO fb_user_stocks (username, number_stocks, total_amount) VALUES (%s, %s, %s)"
        amount_stocks = 5000 + int(number_of_stocks)
        total_amount = amount_stocks * getLatestPrice("FB")
        values = (user, amount_stocks, total_amount)
        facebookcursor.execute(sql, values)
        facebookdb.commit()
    
    else:
        sql = "UPDATE fb_user_stocks SET number_stocks = %s AND total_amount = %s WHERE username = %s"
        new_amount = int(number_of_stocks) + result[0][1]
        total_amount = result[0][2] + (int(number_of_stocks) * getLatestPrice("FB"))
        values = (new_amount, total_amount, user)
        facebookcursor.execute(sql, values)
        facebookdb.commit()

def make_transaction(user, number_of_stocks): # method used to update transaction database
    now = datetime.now()
    dt_string = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    sql = "INSERT INTO fb_user_trnsctns (date, username, number_stocks, total_amount) VALUES (%s, %s, %s, %s)"
    final_amount = int(number_of_stocks) * getLatestPrice("FB")
    values = (dt_string, user, number_of_stocks, final_amount)
    facebookcursor.execute(sql, values)
    facebookdb.commit()

def display_transactions(user): # returns a json object of all transactions
    sql = "SELECT * FROM fb_user_trnsctns WHERE username = %s"
    value = (user, )
    facebookcursor.execute(sql, value)
    row_headers = [x[0] for x in facebookcursor.description]
    result = facebookcursor.fetchall()

    if len(result) == 0:
        return "No transactions for this user"
    else:
        json_data = []
        for r in result:
            json_data.append(dict(zip(row_headers, r)))
        return json.dumps(json_data, indent=4, sort_keys=True, default=str)

def display_stocks(user): # fetches number of stocks and total value of a specific user
    sql = "SELECT * FROM fb_user_stocks WHERE username = %s"
    value = (user, )
    facebookcursor.execute(sql, value)
    result = facebookcursor.fetchall()

    final_arr = [] # array of 2 values, one is number of stocks, other is total value
    if len(result) == 0:
        final_arr.append(5000)
        final_arr.append(5000 * getLatestPrice("FB"))
    else:
        final_arr.append(result[0][1])
        final_arr.append(result[0][2])
    
    return final_arr
    


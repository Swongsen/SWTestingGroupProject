import connect
from aapl import getLatestPrice
from datetime import datetime
import json

fbdb = connect.db
fbcursor = connect.cursor

fbcursor.execute("CREATE DATABASE IF NOT EXISTS fb")
fbcursor.execute("USE fb")

fbcursor.execute("CREATE TABLE IF NOT EXISTS transactions(accountid INTEGER NOT NULL, amount INTEGER NOT NULL, price DOUBLE NOT NULL, created_at TEXT NOT NULL)"

def fb_buy(account, amount):

    #update facebook's transaction log
    sql = "INSERT INTO transactions(accountid, amount, price, created_at) VALUES (%s, %s, %s, %s, NOW())"
    price = getLatestPrice("FB")
    values = (account, amount, price)
    fbcursor.execute(sql, values)
    fbdb.commit()

    #update accounts database
    fbcursor.execute("USE accounts")
    sql = "SELECT funds, fb FROM accounts WHERE accountid = %s"
    values = (account, )
    fbcursor.execute(sql, values)

    #subtract funds from account, add stocks to account
    total_funds = float(fbcursor.fetchone()[0])
    total_stocks = int(fbcursor.fetchone()[1])
    funds_left = total_funds - (price * amount)
    stocks_left = total_stocks + amount
    sql = "UPDATE accounts SET funds = %s AND fb = %s WHERE accountid = %s"
    values = (funds_left, stocks_left, account)
    fbcursor.execute(sql, values)





'''def make_transaction(user, number_of_stocks): # method used to update transaction database
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
    
    return final_arr'''
    


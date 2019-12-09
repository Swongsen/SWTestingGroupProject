from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from auth import auth
from services import monitoring, obs, aapl, fb, nflx, amzn

webclient = Flask(__name__, static_url_path='', static_folder='web_front/static', template_folder='web_front/templates')
webclient.secret_key = "secretkey"

@webclient.route("/")
def reroute():
    return redirect("/login")

@webclient.route("/login", methods=["GET", "POST"])
def login():
    message = None
    test = fb.getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "fb")
    print(test)
    # If a user is already logged in, log them out
    if(session.get("logged_in") == True):
        session.clear()

    if request.method == "POST":
        # Use custom auth module to login
        session["userid"], message = auth.login(session, request)

        if session.get("logged_in"):
            # log, then redirect
            monitoring.log("authentication", (session["userid"], request.form["username"]))
            return redirect("/home")

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template("login.html", message=message)

@webclient.route("/createuser", methods=["GET", "POST"])
def createUser():
    message = None
    if request.method == "POST":
        # Use custom auth module to create account
        message = auth.createUser(session, request)

    return render_template("createuser.html", message=message)

@webclient.route("/home", methods=["GET", "POST"])
def home():
    # Gets the amount of money each stock is currently worth
    aaplprice = aapl.getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "aapl")
    amznprice = amzn.getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "amzn")
    fbprice = fb.getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "fb")
    nflxprice = nflx.getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "nflx")

    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        accounts = obs.viewAccounts()
        num_accounts = len([account["userid"] for account in accounts if account["userid"]==session["userid"]])
        return render_template("home.html",session=session,accounts=accounts,num_accounts=num_accounts, aapl=aaplprice, amzn = amznprice, fb = fbprice, nflx = nflxprice)

@webclient.route("/addaccount", methods=["GET", "POST"])
def addAccount():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            account_name = request.form["account"]
            amount = request.form["amount"]
            obs.addAccount(session["userid"], account_name, amount)
            return redirect("/home")
        return render_template("addaccount.html")

@webclient.route("/selectaccount/accountid=<accountid>", defaults={"accountname": None})
@webclient.route("/selectaccount/accountid=<accountid>&accountname=<accountname>")
def selectAccount(accountid, accountname):
    session["accountid"] = accountid
    session["accountname"] = accountname
    session["token"] = accountid
    return redirect("/home")

@webclient.route("/accounts", methods=["GET"])
def viewAccounts():
    return jsonify(obs.viewAccounts())

@webclient.route("/buy/ticker=<ticker>&amount=<amount>&key=<key>")
def buy(ticker, amount, key):
    obs.buyShares(key, ticker, amount)
    return redirect("/home")

@webclient.route("/sell/ticker=<ticker>&amount=<amount>&key=<key>")
def sell(ticker, amount, key):
    obs.sellShares(key, ticker, amount)
    return redirect("/home")

@webclient.route("/price/ticker=<ticker>&key=<key>")
def getPrice(ticker, key, method=["GET"]):
    if ticker == "aapl":
        return jsonify(aapl.getLatestPrice(key))
    if ticker == "fb":
        return jsonify(fb.getLatestPrice(key))
    if ticker == "amzn":
        return jsonify(amzn.getLatestPrice(key))
    elif ticker == "nflx":
        return jsonify(amzn.getLatestPrice(key))

@webclient.route("/sellstocks", methods=["GET","POST"])
def sellStocks():
     if not session.get('logged_in'):
        return redirect("/login")
     else:
        if request.method == "POST":
            amount = request.form["amount"]
            ticker = request.form["ticker"]
            return redirect("/sell/ticker={}&amount={}&key={}".format(ticker,amount,session["accountid"]))
        return render_template("sellstocks.html")

@webclient.route("/buystocks", methods=["GET","POST"])
def buyStocks():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            amount = request.form["amount"]
            ticker = request.form["ticker"]
            return redirect("/buy/ticker={}&amount={}&key={}".format(ticker,amount,session["accountid"]))
        return render_template("buystocks.html")

@webclient.route("/addfunds", methods=["GET","POST"])
def addFunds():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            money = request.form["money"]
            obs.addFunds(session["accountid"], money)
            # information format = (ticker, userid, accountid, type, amount, price)
            monitoring.log("transaction", (session["userid"], session["accountid"], "fund transfer", "NULL", money))
            return redirect("/home")
        return render_template("addfunds.html")

@webclient.route("/logs/authentication", methods=["GET"])
def viewAuthenticationLogs():
    if not session.get('logged_in'):
        return redirect("/login")
    return monitoring.viewAuthenticationLogs()

@webclient.route("/logs/transaction", methods=["GET"])
def viewTransactionLogs():
    if not session.get('logged_in'):
        return redirect("/login")
    if session["userid"] == 0:
        return monitoring.viewTransactionLogs()
    else:
        return "This page is for admins only"

@webclient.route("/logs/stocktransaction/<ticker>", methods=["GET"])
def viewStockTransactionLogs(ticker):
    if not session.get('logged_in'):
        return redirect("/login")
    return monitoring.viewStockTransactionLogs(ticker)

if __name__ == "__main__":
    webclient.run()

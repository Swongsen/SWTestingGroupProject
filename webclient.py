from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from auth import auth
from services import monitoring, obs, aapl, fb, nflx, amzn

webclient = Flask(__name__)
webclient.secret_key = "secretkey"

@webclient.route("/")
def reroute():
    return redirect("/login")

@webclient.route("/login", methods=["GET", "POST"])
def login():
    message = None

    # If a user is already logged in, log them out
    if(session.get("logged_in") == True):
        session.pop("logged_in", None)

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
def load():
    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        return render_template("home.html")

@webclient.route("/addaccount", methods=["GET", "POST"])
def addAccount():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            account_name = request.form["account"]
            amount = request.form["amount"]
            obs.addAccount(session["userid"], account_name, amount)
            return render_template("/home.html")
        return render_template("addaccount.html")

@webclient.route("/selectaccount/accountname=<accountname>")
def selectAccount(accountname):
    session["token"] = accountname
    return "Selected "+accountname

@webclient.route("/logs/authentication", methods=["GET"])
def viewAuthenticationLogs():
    return monitoring.viewAuthenticationLogs()

@webclient.route("/logs/transaction", methods=["GET"])
def viewTransactionLogs():
    return monitoring.viewTransactionLogs()

@webclient.route("/logs/stocktransaction", methods=["GET"])
def viewStockTransactionLogs():
    return monitoring.viewStockTransactionLogs()

@webclient.route("/accounts", methods=["GET"])
def viewAccounts():
    return obs.viewAccounts()

@webclient.route("/sellstocks", methods=["GET"])
def sellStocks():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            account_name = request.form["account"]
            amount = request.form["amount"]
            obs.sellStocks(session["userid"], account_name, amount)
            return render_template("/home.html")
        return render_template("sellstocks.html")

@webclient.route("/buystocks", methods=["GET"])
def buystocks():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            account_name = request.form["account"]
            amount = request.form["amount"]
            obs.buyStocks(session["userid"], account_name, amount)
            return render_template("/home.html")
        return render_template("buystocks.html")

@webclient.route("/buy/ticker=<ticker>&amount=<amount>&key=<key>")
def buy(ticker, amount, key):
    message = None
    if ticker == "aapl":
        message = aapl.buy(amount, key)
    return jsonify(message)

@webclient.route("/sell/ticker=<ticker>&amount=<amount>&key=<key>")
def sell(ticker, amount, key):
    message = None
    if ticker == "aapl":
        message = aapl.sell(amount, key)
    return jsonify(message)

@webclient.route("/price/ticker=<ticker>&key=<key>")
def getPrice(ticker, key, method=["GET"]):
    if ticker == "aapl":
        return jsonify(aapl.getLatestPrice(key))

@webclient.route("/checkfunds", methods=["GET"])
def checkFunds():
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        if request.method == "POST":
            account_name = request.form["account"]
            amount = request.form["amount"]
            obs.checkFunds(session["userid"], account_name, amount)
            return render_template("/home.html")
        return render_template("checkfunds.html")
if __name__ == "__main__":
    webclient.run()

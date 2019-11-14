from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from auth import auth
from services import monitoring
from services import obs

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
        session["token"], message = auth.login(session, request)

        if session.get("logged_in"):
            # log, then redirect
            monitoring.log("authentication", (session["token"], request.form["username"]))
            return redirect("/home")

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template("login.html", message=message)

@webclient.route("/createuser", methods=["GET", "POST"])
def createUser():
    message = None
    if request.method == "POST":
        # Use custom auth module to create account
        message = auth.createUser(session, request)

    return render_template("createaccount.html", message=message)

@webclient.route("/home", methods=["GET", "POST"])
def load():
    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        return render_template("home.html")

@webclient.route("/addaccount", methods=["GET", "POST"])
def addAccount():
    obs.addAccount(session["token"], 2000)
    return "Account created"

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

if __name__ == "__main__":
    webclient.run()

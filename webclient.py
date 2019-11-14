from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from auth import auth

webclient = Flask(__name__)
webclient.secret_key = "secretkey"
token = None

@webclient.route("/")
def reroute():
    return redirect("/login")

@webclient.route("/login", methods=["GET", "POST"])
def login():
    # global token so that it actually changes when modified in this function
    global token
    message = None

    # If a user is already logged in, log them out
    if(session.get("logged_in") == True):
        session.pop("logged_in", None)

    if request.method == "POST":
        # Use custom auth module to login
        token, message = auth.login(session, request)

        if session.get("logged_in"):
            return redirect("/home")

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template("login.html", message=message)

@webclient.route("/createaccount", methods=["GET", "POST"])
def create():
    message = None
    if request.method == "POST":
        # Use custom auth module to create account
        message = auth.createAccount(session, request)

    return render_template("createaccount.html", message=message)

@webclient.route("/home", methods=["GET", "POST"])
def load():
    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        return render_template("home.html")

if __name__ == "__main__":
    webclient.run()

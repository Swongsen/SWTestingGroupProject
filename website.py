from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

website = Flask(__name__)
# Makeshift login token
token = 0

@website.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        # Get the username and password from the request form
        user = request.form["username"]
        password = request.form["password"]

        user_data = pd.read_csv("users.csv")

        # Reads the users csv to validate username password
        for index, row in user_data.iterrows():
            # If the username, password matches the username and password from the form
            if user == row["user"] and password == row["password"]:
                token = 1
                return redirect("/home")
            else:
                message = "Invalid Credentials"

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template("login.html", message=message)

@website.route("/createaccount", methods=["GET", "POST"])
def create():
    message = None
    if request.method == "POST":
        # Get the username and password from the request form
        user = request.form["username"]
        password = request.form["password"]

        user_data = pd.read_csv("users.csv")
        user_data = user_data.set_index("id")

        account_exists = False
        # Reads the users csv to validate username does not already exist
        for index, row in user_data.iterrows():
            # If the username exists in csv, account exists
            if user == row["user"]:
                account_exists = True

        if account_exists:
            message = "User already exists"
        else:
            user_data = user_data.append({"user":user, "password": password}, ignore_index=True)
            user_data.to_csv('users.csv', index_label = "id")
            message = "Account successfully created"

    return render_template("createaccount.html", message=message)

@website.route("/home")
def load():
    return render_template('home.html')















website.run()

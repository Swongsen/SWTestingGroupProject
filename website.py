from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

website = Flask(__name__)

website.secret_key = 'secretkey'
# Makeshift login token
token = 0

@website.route("/login", methods=["GET", "POST"])
def login():
    message = None

    # If a user is already logged in, log them out
    if(session.get('logged_in') == True):
        session.pop('logged_in', None)

    if request.method == "POST":
        # Get the username and password from the request form
        user = request.form["username"]
        password = request.form["password"]

        user_data = pd.read_csv("users.csv")

        # Reads the users csv to validate username password
        for index, row in user_data.iterrows():
            # If the username, password matches the username and password from the form
            if user == row["user"] and password == row["password"]:
                # Since there is match from users.csv, set the session to be logged in
                session['logged_in'] = True
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

        if(len(password) < 8):
            message = "Password too short"
            return render_template("createaccount.html", message=message)

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

@website.route("/home", methods=["GET", "POST"])
def load():
    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
        return render_template("home.html")















website.run()

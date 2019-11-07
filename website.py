from flask import Flask, render_template, request, redirect, url_for, session
import csv

website = Flask(__name__)
# Makeshift login token
token = 0

@website.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Get the username and password from the request form
        User = request.form['username']
        Pass = request.form['password']
        #print(User + ' ' + Pass)


        # Reads the users csv to validate username password
        with open('users.csv', newline='') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csvreader:
                # Prints out the top row of csv
                if line_count == 0:
                    # print(f'Column names: {", ".join(row)}')
                    line_count += 1
                # If the username, password matches the username and password from the form
                else:
                    if User == row[0] and Pass == row[1]:
                        token = 1
                        return redirect('/home')
                    else:
                        error = 'Invalid Credentials'

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template('login.html', error=error)

@website.route('/createaccount')
def create():
    return "hello"

@website.route('/home')
def load():
    return render_template('home.html')















website.run()

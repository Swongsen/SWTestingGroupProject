import mysql.connector

# Config values
db_host = "34.73.169.74"
db_user = "root"
db_password = "cis4930"

# Connects to database, set up cursor
try:
    db = mysql.connector.connect(host=db_host,user=db_user,password=db_password)
except:
    print("Could not connect to OBS database, is it up?")

cursor = db.cursor()
import pandas as pd
from services import connect

cur = connect.cursor

""" ACCOUNT MANAGEMENT """
# Add an account with starting $ for a user
def addAccount(user, starting_balance):
    return 1

# View balance for a given account
def viewAccountBalance(account):
    return 1

""" TRANSACTIONS """
# Add money to a given account
def addFunds(account):
    return 1

# Buy an amount of shares of a certain ticker for an account
def buyShare(account, ticker, amount):
    return 1

# Sell an amount of shares of a certain ticker for an account
def sellShare(account, ticker, amount):
    return 1

""" NET WORTH """
# Get total account balances and shares owned
def netWorth(user):
    return 1
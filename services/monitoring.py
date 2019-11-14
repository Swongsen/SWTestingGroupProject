import pandas as pd
import MySQLdb

# log function that should be able to log anything
# classification should be either: 
# authentication, transaction, or stock transaction
def log(classification, information):
    return 1

# ADMIN VIEW OF LOGS
# No login required
def viewAuthenticationLogs():
    return 1

def viewTransactionLogs():
    return 1

def viewStockTransactions():
    return 1
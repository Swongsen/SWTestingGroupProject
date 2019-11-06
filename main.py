from iexfinance.stocks import Stock
import pandas as pd

# get latest price when given ticker
def getLatestPrice(ticker):
    stock = Stock(ticker, token="pk_f5f73c6bf9c44432be834bb284253a11")
    latest_price = stock.get_quote()["latestPrice"]
    return latest_price

print(getLatestPrice("FB"))
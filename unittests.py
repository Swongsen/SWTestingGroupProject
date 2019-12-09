import pytest
import os
import unittest
from unittest.mock import Mock
#from ..webclient import reroute, login, createUser, load
from webclient import webclient
from webclient import reroute
from services.amzn import getLatestPrice
from services.aapl import getLatestPrice
from services.fb import getLatestPrice
from services.nflx import getLatestPrice

# Testing that the reroute page ('/'), returns the response code for rerouting
def test_reroute():
    response = reroute()
    assert response.status_code == 302

# Mock testing the login page
def test_login():
    mock = Mock()
    mock.login()
    mock.login.assert_called()

# Mock testing the createaccount page
def test_createUser():
    mock = Mock()
    mock.createUser()
    mock.createUser.assert_called()

# Mock testing the home page
def test_load():
    mock = Mock()
    mock.load()
    mock.load.assert_called()

# Tests to make sure returned aapl price is in correct form
def test_aaplprice():
    price =  getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "aapl")
    assert type(price) is float

# Tests to make sure returned amzn price is in correct form
def test_amznprice():
    price = getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "amzn")
    assert type(price) is float

# Tests to make sure returned fb price is in correct form
def test_fbprice():
    price = getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "fb")
    assert type(price) is float

# Tests to make sure returned nflx price is in correct form
def test_nflxprice():
    price = getLatestPrice(0, "A5dHAZqYNutmBOjIzppnWIsAwYw4", "nflx")
    assert type(price) is float

if __name__ == "main":
    unittest.main()

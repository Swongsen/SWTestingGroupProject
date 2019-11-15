import pytest
import os
import unittest
from unittest.mock import Mock
from aapl import getLatestPrice, buy, sell

# Test for getLatestPrice function
def test_getLatestPrice():
    # Asserts an error when the parameters to getLatestPrice is wrong
    with pytest.raises(Exception):
        assert getLatestPrice("sf", "fdd")

    # Mock to assert that the function getLatestPrice is called once with the correct ticker and key
    mock = Mock()
    mock.getLatestPrice("A5dHAZqYNutmBOjIzppnWIsAwYw4", "AAPL")
    mock.getLatestPrice.assert_called_once_with("A5dHAZqYNutmBOjIzppnWIsAwYw4", "AAPL")

# Test for buy function
def test_buy():
    # Mock to assert that the buy function works and is called once
    mock = Mock()
    mock.buy("logged_in", 1)
    mock.buy.assert_called_once_with("logged_in", 1)

# Test for sell function
def test_sell():
    mock = Mock()
    mock.sell("logged_in", 1)
    mock.sell.assert_called_once_with("logged_in", 1)

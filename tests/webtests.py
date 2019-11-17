import pytest
import os
import unittest
from unittest.mock import Mock
#from ..webclient import reroute, login, createUser, load
from webclient import webclient

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

if __name__ == "main":
    unittest.main()

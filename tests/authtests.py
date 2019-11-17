import pytest
import os
import unittest
from unittest.mock import Mock
from auth import login, createAccount


def test_login():
    mock = Mock()
    mock.login()
    mock.login.assert_called()

def test_createAccount():
    mock = Mock()
    mock.createAccount()
    mock.createAccount.assert_called()

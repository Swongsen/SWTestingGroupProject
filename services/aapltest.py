import pytest
import os
import unittest
from unittest.mock import Mock
from aapl import getLatestPrice

def test_getLatestPrice():
    with pytest.raises(Exception):
        assert getLatestPrice("sf", "fdd")

    mock = Mock()
    mock.getLatestPrice("A5dHAZqYNutmBOjIzppnWIsAwYw4", "AAPL")
    mock.getLatestPrice.assert_called_once_with("A5dHAZqYNutmBOjIzppnWIsAwYw4", "AAPL")

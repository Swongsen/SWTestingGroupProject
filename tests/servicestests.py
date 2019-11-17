import pytest
import os
import unittest
from unittest.mock import Mock
from obs.py import addAccount, viewAccountBalance, addFunds, buyShare, sellShare, netWorth
from monitoring.py import log, viewAuthenticationLogs
from aapl.py import getLatestPrice

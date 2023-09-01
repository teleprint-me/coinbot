"""
coinbot/api/alpaca.py
"""
import hashlib
import hmac
import time
from datetime import datetime as dt
from os import getenv
from typing import Any, Dict, List, Optional, Union

# NOTE: Always generate uuid4 for privacy!
from uuid import uuid4

import requests
from dotenv import load_dotenv
from requests import RequestException
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbot import __agent__, __source__, __version__

__paper__ = "https://paper-api.alpaca.markets"
__alpaca__ = "https://api.alpaca.markets"


class Auth(AuthBase):
    """Create and return an HTTP request with authentication headers.

    Args
        api: Instance of the API class, if not provided, a default instance is created.
    """

    pass

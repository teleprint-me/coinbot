"""
coinbot/api/alpaca.py
"""
import time
from os import getenv
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv
from requests import RequestException
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbot import __agent__, __source__, __version__, logging

load_dotenv()

# Rate limit of API requests in seconds.
# Basic is free and allows 200 API calls/min
# Plus is $99/mo and allows 10,000 API calls/min
# We default to Basic which allows 200 calls/min
__limit__: float = 1 / (200 / 60)

# Timeout value for HTTP requests.
__timeout__: int = 30

# Paper trading URL differs from live trading
__paper__ = "https://paper-api.alpaca.markets"

# Use the live trading URL
__alpaca__ = "https://api.alpaca.markets"


class Auth(AuthBase):
    """Create and return an HTTP request with authentication headers.

    Args
        api: Instance of the API class, if not provided, a default instance is created.
    """

    def __init__(self):
        """Create an instance of the Auth class.

        Args:
            api: Instance of the API class, if not provided, a default instance is created.
        """

        self.key: Optional[str] = (
            getenv("ALPACA_API_KEY") or getenv("PAPER_ALPACA_API_KEY") or ""
        )
        self.secret: Optional[str] = (
            getenv("ALPACA_API_SECRET") or getenv("PAPER_ALPACA_API_SECRET") or ""
        )

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """Return the prepared request with updated headers.

        Args:
            request: A prepared HTTP request.

        Returns:
            The same request with updated headers.
        """

        # Sign and authenticate payload.
        header: Dict = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "APCA-API-KEY-ID": self.key,
            "APCA-API-SECRET-KEY": self.secret,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Inject payload
        request.headers.update(header)

        return request


__auth__ = Auth()


def get(url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Perform a GET request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        data: (optional) Query parameters to be passed with the request.

    Returns:
        The response of the GET request.
    """

    time.sleep(__limit__)

    try:
        response = requests.get(
            url=url,
            params=data,
            auth=__auth__,
            timeout=__timeout__,
        )

        if response.status_code != 200:
            error_message = response.json()["message"]

        if response.status_code == 400:
            raise RequestException(f"400 Bad Request: {error_message}")
        elif response.status_code == 401:
            raise RequestException(f"401 Unauthorized: {error_message}.")
        elif response.status_code == 403:
            raise RequestException(f"403 Forbidden: {error_message}.")
        else:
            return response
    except RequestException as error:
        raise RequestException(error)


def get_crypto_candlesticks(loc: str, data: dict[str, Any]) -> dict[str, List]:
    """
    Fetches historical crypto candlestick data from the Alpaca API.

    Args:
        loc (str): Crypto location, e.g., "us".
        data (dict[str, Any]): Parameters for the API request.

    Returns:
        dict[str, List]: Historical candlestick data for specified symbols.
    """
    url = f"https://data.alpaca.markets/v1beta3/crypto/{loc}/bars"
    response = get(url, data=data)
    data = response.json()

    if response.status_code != 200:
        error = data.get("message", "Error retrieving candlesticks from Alpaca API")
        logging.error(f"RequestError: {response.status_code}: {error}")
        return {}

    return data.get("bars", {})

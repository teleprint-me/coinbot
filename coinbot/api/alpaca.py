"""
coinbot/api/alpaca.py
"""
import time
from collections import defaultdict
from os import getenv
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from requests import RequestException, Response
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


def get(url: str, params: Optional[Dict] = None) -> Response:
    """Perform a GET request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        params: (optional) Query parameters to be passed with the request.

    Returns:
        The response of the GET request.
    """

    time.sleep(__limit__)

    try:
        response = requests.get(
            url=url,
            params=params,
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


def get_crypto_candlesticks(loc: str, params: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Fetches historical crypto candlestick data from the Alpaca API.

    Args:
        loc (str): Crypto location, e.g., "us".
        params (dict[str, Any]): Parameters for the API request.

    Returns:
        Dict[str, List[Dict]]: Historical candlestick data for specified symbols.
    """
    url = f"https://data.alpaca.markets/v1beta3/crypto/{loc}/bars"
    # NOTE: `get` is a magic function that handles `requests` under the hood.
    response: Response = get(url, params=params)
    json_data: Dict[str, Any] = response.json()

    if response.status_code != 200:
        error = json_data.get("message", "Error getting candlesticks from Alpaca API")
        logging.error(f"GetError: {response.status_code}: {error}")
        return {}

    return json_data.get("bars", {})


def page_crypto_candlesticks(loc: str, params: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Fetches paginated historical crypto candlestick data from the Alpaca API.

    Retrieves candlestick data for specified crypto assets, handling pagination if applicable.

    Args:
        loc (str): Crypto location, e.g., "us".
        params (Dict[str, Any]): Parameters for the API request.

    Returns:
        Dict[str, List[Dict]]: Historical candlestick data for specified symbols, paginated if needed.
    """
    url = f"https://data.alpaca.markets/v1beta3/crypto/{loc}/bars"
    all_bars = defaultdict(list)

    while True:
        # NOTE: `get` is a magic function that handles `requests` under the hood.
        response: Response = get(url, params=params)
        json_data: Dict[str, Any] = response.json()

        if response.status_code != 200:
            error = json_data.get(
                "message", "Error paging candlesticks from Alpaca API"
            )
            logging.error(f"PageError: {response.status_code}: {error}")
            break

        bars = json_data.get("bars", {})
        if not bars:
            break

        for asset_pair, asset_bars in bars.items():
            all_bars[asset_pair].extend(asset_bars)

        next_page_token = json_data.get("next_page_token", None)
        if next_page_token is None:
            break

        params["page_token"] = next_page_token

    return dict(all_bars)  # Convert defaultdict back to a regular dictionary.

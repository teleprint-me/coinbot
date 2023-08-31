"""
coinbot/coinbase.py
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

load_dotenv()

# Rate limit of API requests in seconds.
# Calculated as 1 / (n requests_per_hour / m seconds_per_hour)
# Rate limit used to block request for at least 0.1 seconds.
__limit__: float = 1 / (36000 / 3600)

# Timeout value for HTTP requests.
__timeout__: int = 30

# Sign In lets Coinbase users easily and securely sign in to your product or service,
# and lets you integrate Coinbase supported cryptocurrencies into your applications.
__coinbase__: str = "https://api.coinbase.com/v2"

# Coinbase Advanced Trade replaces and improves upon Coinbase Pro.
# Advanced Trade API supports programmatic trading and order management with a REST API
# and WebSocket protocol for real-time market data.
__advanced__: str = "https://api.coinbase.com/api/v3/brokerage"


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

        self.key: Optional[str] = getenv("API_KEY") or ""
        self.secret: Optional[str] = getenv("API_SECRET") or ""

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """Return the prepared request with updated headers.

        Args:
            request: A prepared HTTP request.

        Returns:
            The same request with updated headers.
        """

        # Create payload.
        timestamp: str = str(int(time.time()))
        body: str = "" if not request.body else request.body.decode("utf-8")
        method: str = "" if not request.method else request.method.upper()
        message: str = f"{timestamp}{method}{request.path_url}{body}"

        # Create signature.
        key = self.secret.encode("ascii")
        msg = message.encode("ascii")
        signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

        # Sign and authenticate payload.
        header: Dict = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "CB-ACCESS-KEY": self.key,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-VERSION": "2021-08-03",
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

        if response.status_code == 401:
            raise RequestException(
                "401 Unauthorized: Client failed to authenticate the request."
            )
        elif response.status_code == 403:
            raise RequestException(
                "403 Forbidden: Client failed to authorize the necessary scope."
            )
        elif "errors" in response and "message" in response["errors"]:
            raise RequestException(response["errors"]["message"])
        elif "error" in response and "error_description" in response["error"]:
            raise RequestException(response["error"]["error_description"])
        elif "error" in response and "message" in response["error"]:
            raise RequestException(response["error"]["message"])
        else:
            return response
    except RequestException as error:
        raise RequestException(f"Error retrieving GET request: {error}")


def post(url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Perform a POST request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        data: (optional) JSON payload to be sent with the request.

    Returns: The response of the POST request.
    """

    time.sleep(__limit__)

    try:
        response = requests.post(
            url=url,
            json=data,
            auth=__auth__,
            timeout=__timeout__,
        )

        if response.status_code == 401:
            raise RequestException(
                "401 Unauthorized: Client failed to authenticate the request."
            )
        elif response.status_code == 403:
            raise RequestException(
                "403 Forbidden: Client failed to authorize the necessary scope."
            )
        elif "errors" in response and "message" in response["errors"][0]:
            raise RequestException(response["errors"][0]["message"])
        elif "error" in response and "error_description" in response["error"]:
            raise RequestException(response["error"]["error_description"])
        elif "error" in response and "message" in response["error"]:
            raise RequestException(response["error"]["message"])
        else:
            return response
    except RequestException as error:
        raise RequestException(f"Error retrieving POST request: {error}")


def get_candlestick_data(
    product_id: str,
    start: int,
    end: int,
    granularity: str,
) -> List[Dict[str, Union[str, float]]]:
    """Retrieve candlestick data for a trading pair.

    Args:
        product_id: The trading pair (e.g., 'BTC-USD').
        start: Timestamp for starting range of aggregations, in UNIX time.
        end: Timestamp for ending range of aggregations, in UNIX time.
        granularity: The time slice value for each candle.

    Returns:
        List of candlestick data dictionaries.
    """
    url = f"{__advanced__}/products/{product_id}/candles"
    data = {
        "start": start,
        "end": end,
        "granularity": granularity,
    }

    response = get(url, data)

    # Process response and extract candlestick data
    candlestick_data = []

    # Processing logic here

    return candlestick_data


def get_min_order_size(product_id: str) -> float:
    """Get the minimum order size of an asset on Coinbase.

    Args:
        product_id (str): The identifier for the asset.

    Returns:
        float: The minimum order size of the asset.
    """

    url = f"{__advanced__}/products/{product_id}"
    response = get(url).json()

    if "quote_min_size" in response:
        quote_min_size = float(response["quote_min_size"])
        return quote_min_size
    else:
        raise Exception(
            f"Failed to fetch minimum order size for {product_id}. Response: {response}"
        )


def get_spot_price(
    currency_pair: str,
    datetime: Optional[str] = None,
) -> float:
    """Perform a GET request to the coinbase API path for spot prices.

    Args:
        currency_pair: The base and quote currency pair, e.g. "BTC-USD"
        datetime: (optional) For historic spot price, use format YYYY-MM-DD (UTC)

    Returns:
        The response of the GET request as a float representing the spot price

    Raises:
        RequestException: If there's an issue with the response or if the response is missing data
    """

    try:
        url = f"{__coinbase__}/prices/{currency_pair}/spot"

        if datetime:
            response = get(url, data={"date": datetime}).json()
        else:
            response = get(url).json()

        print(response)

        if "data" in response and "amount" in response["data"]:
            return float(response["data"]["amount"])
        else:
            raise RequestException("Invalid response from the API")

    except RequestException as error:
        raise RequestException(f"Error retrieving spot price: {error}")


def get_simulated_market_order(
    quote_size: float,
    product_id: str,
    side: str = "BUY",
) -> Dict[str, Union[str, float]]:
    """Simulate a market order based on current spot price and input parameters.

    Args:
        quote_size: The amount of quote currency to spend on the order (required for BUY orders).
        product_id: The product this order is created for, e.g., 'BTC-USD'.
        side: The side of the order, either 'BUY' or 'SELL'. Defaults to 'BUY'.

    Returns:
        A dictionary containing details of the simulated order, including order_id, product_id, side, principal_amount,
        datetime, market_price, order_size, and order_fee.
    """

    exchange = getenv("EXCHANGE") or "coinbase"
    product_id = getenv("PRODUCT_ID") or product_id
    principal_amount = float(getenv("PRINCIPAL_AMOUNT") or quote_size)

    market_price = get_spot_price(product_id)

    taker_fee = 0.006
    order_fee = principal_amount * taker_fee
    order_size = (principal_amount - order_fee) / market_price

    return {
        "order_id": str(uuid4()),
        "exchange": exchange,
        "product_id": product_id,
        "principal_amount": principal_amount,
        "side": side.upper(),
        "datetime": dt.now().isoformat(),
        "market_price": market_price,
        "order_size": order_size,
        "order_fee": order_fee,
    }


def post_market_order(
    quote_size: float,
    product_id: str,
    side: str = "BUY",
) -> Dict[str, Union[str, float]]:
    """Post a market order to the Coinbase Advanced Trade API.

    Args:
        quote_size: The amount of quote currency to spend on the order (required for BUY orders).
        product_id: The product this order was created for, e.g., 'BTC-USD'.
        side: The side of the order, either 'BUY' or 'SELL'. Defaults to 'BUY'.

    Returns:
        A dictionary containing details of the created order, including order_id, product_id, side, base_size, and quote_size.

    Raises:
        RequestException: If there's an issue with the response or if the response contains an error message.
    """

    try:
        market_order = {
            "client_order_id": str(uuid4()),
            "product_id": product_id,
            "side": side.upper(),
            "order_configuration": {
                "market_market_ioc": {"quote_size": str(quote_size)}
            },
        }

        response = post(f"{__advanced__}/orders", data=market_order)

        if "success" in response and response["success"]:
            url = f"{__advanced__}/orders/historical/{response['order_id']}"
            order_response = get(url).json()
            order = order_response["order"]

            return {
                "order_id": order["order_id"],
                "exchange": "coinbase",
                "product_id": order["product_id"],
                "principal_amount": float(quote_size),
                "side": order["side"],
                "datetime": order["created_time"],
                "market_price": float(order["average_filled_price"]),
                "order_size": float(order["filled_size"]),
                "order_fee": float(order["total_fees"]),
            }

        else:
            raise RequestException(response["error_response"]["message"])

    except RequestException as error:
        raise RequestException(f"Error posting market order: {error}")
        raise RequestException(f"Error posting market order: {error}")

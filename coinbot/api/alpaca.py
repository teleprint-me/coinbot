"""
coinbot/api/alpaca.py
"""
import time
from collections import defaultdict
from json import JSONDecodeError
from os import getenv
from typing import Any, Dict, Generator, List, Optional, Union

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

# Define the Alpaca API sub-domains based on context
ALPACA_SUBDOMAINS = {
    "broker": {
        "paper": "https://broker-api.sandbox.alpaca.markets",
        "live": "https://broker-api.alpaca.markets",
    },
    "trade": {
        "paper": "https://paper-api.alpaca.markets",
        "live": "https://api.alpaca.markets",
    },
    "data": {
        "paper": "https://data.sandbox.alpaca.markets",
        "live": "https://data.alpaca.markets",
    },
}


def normalize_endpoint(endpoint: str) -> str:
    """Normalize the endpoint by adding a leading slash if missing.

    Args:
        endpoint (str): The endpoint to normalize.

    Returns:
        str: The normalized endpoint.
    """
    return endpoint if endpoint.startswith("/") else "/" + endpoint


def get_alpaca_url(subdomain: str, context: str, endpoint: str) -> str:
    """Construct the Alpaca API URL based on sub-domain, context, and endpoint.

    Args:
        subdomain (str): The API sub-domain ("broker", "trade", or "data").
        context (str): The context ("paper" for paper trading, "live" for live trading).
        endpoint (str): The specific endpoint to access.

    Returns:
        str: The full API URL based on the provided parameters.

    Example:
        trade_api_url = get_alpaca_url("trade", "live", "/v2/orders")
        print(trade_api_url)
    """
    normalized_endpoint = normalize_endpoint(endpoint)
    return f"{ALPACA_SUBDOMAINS[subdomain][context]}{normalized_endpoint}"


def get_alpaca_endpoint(subdomain: str, endpoint: str, live: bool = False) -> str:
    """Constructs the Alpaca API endpoint based on sub-domain and live flag.

    Args:
        subdomain (str): The API sub-domain ("broker", "trade", or "data").
        endpoint (str): The specific endpoint to access.
        live (bool): Whether to use live trading data. Default is False.

    Returns:
        str: The constructed API endpoint.
    """
    context = "live" if live else "paper"
    return get_alpaca_url(subdomain, context, endpoint)


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

        return response
    except RequestException as error:
        raise RequestException(error)


def post(url: str, json: Optional[Dict] = None) -> Response:
    """Perform a POST request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        json: (optional) JSON payload to be sent with the request.

    Returns:
        The response of the POST request.
    """
    time.sleep(__limit__)

    try:
        response = requests.post(
            url=url,
            json=json,
            auth=__auth__,
            timeout=__timeout__,
        )

        return response
    except RequestException as error:
        raise RequestException(error)


def page(url: str, params: Optional[Dict] = None) -> Generator[Response, None, None]:
    """Pages through API responses.

    Args:
        url (str): API endpoint URL.
        params (Optional[Dict]): Query parameters for the API call.

    Yields:
        Response: HTTP Response object for each page.
    """

    next_page_token = None  # Initialize the page token

    while True:
        if next_page_token is not None:
            params = params or {}
            params["page_token"] = next_page_token

        # Perform a GET request to the specified API path.
        response = get(url, params=params)
        yield response

        try:
            json_data = response.json()
            next_page_token = json_data.get("next_page_token")
        except JSONDecodeError as message:
            logging.error(message)
            raise RequestException(f"Error {response.status_code}: {response.text}")

        if next_page_token is None:
            break


def get_json_data(response: Response) -> Dict[str, Any]:
    """Process the HTTP Response.

    Args:
        response (Response): The HTTP Response object.

    Returns:
        Dict: The JSON-decoded content of the HTTP response.

    Raises:
        RequestException: If the response contains an error.
    """
    try:
        json_data = response.json()

        if response.status_code != 200:
            error_message = json_data.get("message", "Unknown error")
            raise RequestException(f"Error ({response.status_code}): {error_message}")

        return json_data

    except JSONDecodeError as message:
        logging.error(message)
        raise RequestException(f"Error ({response.status_code}): {response.text}")


def get_clock(live: bool = True) -> Dict[str, Union[str, bool]]:
    """Returns the market clock.

    The clock API serves the current market timestamp, whether or not the market is currently open, as well as the times of the next market open and close.

    Keys are timestamp, is_open, next_open, and next_close.

    Returns:
        Dict: A dictionary representing whether the market is open or closed.
    """
    endpoint = get_alpaca_endpoint("trade", "/v2/clock", live)
    response = get(endpoint)
    return get_json_data(response)


def get_asset(symbol: str, live: bool = False) -> Dict[str, Any]:
    """Get the asset model for a given Symbol or Asset ID.

    Useful for retrieving the minimum order size, minimum trade increment, and price increment. Note that this will only return information for single asset.

    Returns:
        Dict: A dictionary containing information about the given asset.
    """
    endpoint = get_alpaca_endpoint("trade", f"/v2/assets/{symbol}", live=live)
    response = get(endpoint)
    return get_json_data(response)


def get_current_asset_value(symbol: str, live: bool = False) -> Dict[str, float]:
    """Get the current value and quantity of a specified asset.

    Retrieves the current price, quantity, and market value of a specified asset from the positions API.

    Args:
        symbol (str): The symbol of the asset (e.g., "AAPL", "BTC/USD").
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        Dict[str, float]: A dictionary containing current price, quantity, and market value.
    """
    if "/" in symbol:
        products = symbol.split("/")
        symbol = "".join(products)

    endpoint = get_alpaca_endpoint("trade", "/v2/positions", live)
    response = get(endpoint)
    positions = get_json_data(response)

    for position in positions:
        if position["symbol"] == symbol:
            return {
                "current_price": float(position["current_price"]),
                "qty": float(position["qty"]),
                "market_value": float(position["market_value"]),
            }

    return {}


def get_latest_crypto_quote(symbol: str, live: bool = False) -> float:
    """Get the latest quote for a cryptocurrency.

    Retrieves the latest bid price for a specific cryptocurrency symbol from the crypto quote API.

    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., "BTC/USD").
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        float: The latest bid price for the cryptocurrency.
    """
    endpoint = get_alpaca_endpoint(
        "data", "/v1beta3/crypto/us/latest/quotes", live=live
    )
    response = get(endpoint, params={"symbols": symbol})
    data = get_json_data(response)
    # 'bp' is the last bid price
    return float(data["quotes"][symbol]["bp"])


def get_latest_stock_quote(symbol: str, feed: str = "sip", live: bool = False) -> float:
    """Get the latest quote for a stock.

    Retrieves the latest bid price for a specific stock symbol from the stock quote API.

    Args:
        symbol (str): The symbol of the stock (e.g., "AAPL").
        feed (str, optional): The data feed to use. Default is "sip".
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        float: The latest bid price for the stock.
    """
    endpoint = get_alpaca_endpoint("data", "/v2/stocks/quotes/latest", live)
    response = get(endpoint, params={"symbols": symbol, "feed": feed})
    data = get_json_data(response)
    # 'bp' is the last bid price
    return float(data["quotes"]["quotes"][symbol]["bp"])


def get_current_market_price(
    symbol: str, feed: str = "sip", asset_class: str = "stock", live: bool = False
) -> float:
    """Get the current market price of an asset.

    Fetches and returns the current market price of an asset, either a stock or cryptocurrency.

    Args:
        symbol (str): The symbol of the asset (e.g., "AAPL", "BTC/USD").
        feed (str, optional): The data feed to use. Default is "sip".
        asset_class (str, optional): The class of the asset ("stock" or "crypto"). Default is "stock".
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        float: The current market price of the asset.

    Raises:
        ValueError: If an unsupported asset class is provided.
    """
    if asset_class == "crypto":
        return get_latest_crypto_quote(symbol, live)
    elif asset_class == "stock":
        return get_latest_stock_quote(symbol, feed, live)
    else:
        raise ValueError(f"Unsupported asset class: {asset_class}")


def get_crypto_candlesticks(
    loc: str, params: Dict[str, Any], live: bool = True
) -> Dict[str, List[Dict]]:
    """Fetches historical crypto candlestick data from the Alpaca API.

    Args:
        loc (str): Crypto location, e.g., "us".
        params (dict[str, Any]): Parameters for the API request.
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        Dict[str, List[Dict]]: Historical candlestick data for specified symbols.
    """
    endpoint = get_alpaca_endpoint("data", f"/v1beta3/crypto/{loc}/bars", live)
    response = get(endpoint, params=params)
    json_data = get_json_data(response)
    return json_data.get("bars", {})


def page_crypto_candlesticks(
    loc: str, params: Dict[str, Any], live: bool = False
) -> Dict[str, List[Dict]]:
    """Fetches paginated historical crypto candlestick data from the Alpaca API.

    Retrieves candlestick data for specified crypto assets, handling pagination if applicable.

    Args:
        loc (str): Crypto location, e.g., "us".
        params (Dict[str, Any]): Parameters for the API request.
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        Dict[str, List[Dict]]: Historical candlestick data for specified symbols, paginated if needed.
    """
    all_bars = defaultdict(list)
    endpoint = get_alpaca_endpoint("data", f"/v1beta3/crypto/{loc}/bars", live=live)

    for response in page(endpoint, params):
        json_data = get_json_data(response)
        bars = json_data.get("bars", {})

        if not bars:
            break

        for asset_pair, asset_bars in bars.items():
            all_bars[asset_pair].extend(asset_bars)

    return dict(all_bars)


def create_order(
    symbol: str,
    quantity: float,
    side: str,
    type_: str,
    time_in_force: str,
    live: bool = False,
) -> Dict:
    """Create an Order.

    Places a new order for the given account. An order request may be rejected if the account is not authorized for trading, or if the tradable balance is insufficient to fill the order.

    Args:
        symbol (str): The symbol of the asset to trade (e.g., "AAPL").
        quantity (float): The quantity of the asset to trade.
        side (str): The side of the order ("buy" or "sell").
        type_ (str): The order type ("market", "limit", etc.).
        time_in_force (str): The time in force for the order ("gtc", "ioc", etc.).
        live (bool, optional): Whether to execute the trade in a live environment. Defaults to False for paper trading.

    Returns:
        Dict: Response from the Alpaca API.
    """
    # Prepare the payload
    payload = {
        "symbol": symbol,
        "qty": quantity,
        "side": side,
        "type": type_,
        "time_in_force": time_in_force,
    }

    # Choose the correct endpoint based on the `live` flag
    endpoint = get_alpaca_endpoint("trade", "/v2/orders", live=live)

    # Execute the POST request
    response = post(endpoint, json=payload)

    return get_json_data(response)


def get_amount_from_orders(symbol: str, live: bool = False) -> float:
    """Get the total quantity of a specified asset from closed and filled orders.

    Retrieves the total filled quantity of a specified asset from closed orders.

    Args:
        symbol (str): The symbol of the asset (e.g., "AAPL", "BTC/USD").
        live (bool, optional): Whether to use live trading data. Default is False.

    Returns:
        float: The total filled quantity of the asset from closed orders.
    """
    total_qty = 0.0
    endpoint = get_alpaca_endpoint("broker", "/v2/orders", live=live)
    params = {
        "status": "closed",
        "symbol": symbol,
    }

    response = get(endpoint, params=params)
    orders = get_json_data(response)

    for order in orders:
        if order["symbol"] == symbol and order["status"] == "filled":
            total_qty += float(order["filled_qty"])

    return total_qty

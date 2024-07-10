"""
coinbot/api/alpaca/trade.py
"""
from typing import Any, Dict, List, Optional

from coinbot.api.alpaca.auth import AlpacaAuth
from coinbot.api.alpaca.rest import AlpacaREST


class AlpacaTrader(AlpacaREST):
    """A class for interacting with the Alpaca Trade API."""

    def __init__(
        self,
        auth: Optional[AlpacaAuth] = None,
        rate_limit: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize an instance of AlpacaTrader.

        Args:
            auth (AlpacaAuth, optional): An instance of the AlpacaAuth class for authentication.
                If not provided, it will use defaults or authentication from the .env file.
            rate_limit (float, optional): The rate limit for API requests in seconds.
                Defaults to 200 API calls per minute for the free Basic plan.
            timeout (int, optional): Timeout value for HTTP requests in seconds.
                Defaults to 30 seconds.
        """
        super().__init__(auth, rate_limit, timeout)

    def get_clock(self, live: bool = False) -> Dict[str, Any]:
        """
        Get the current market clock information.

        Retrieves information about the current market time, whether it's open, and the next open/close times.

        Args:
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            Dict[str, Any]: Information about the market clock.
        """
        endpoint = self.endpoint.build("trade", "/v2/clock", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_account(self, live: bool = False) -> Dict[str, Any]:
        """Returns the account associated with the API key."""
        endpoint = self.endpoint.build("trade", "/v2/account", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_all_orders(self, live: bool = False) -> List[Dict[str, Any]]:
        """Retrieves a list of orders for the account, filtered by the supplied query parameters."""
        endpoint = self.endpoint.build("trade", "/v2/orders", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_order(
        self, order_id: str, nested: bool = False, live: bool = False
    ) -> Dict[str, Any]:
        """Retrieves a single order for the given order_id."""
        endpoint = self.endpoint.build("trade", f"/v2/orders/{order_id}", live)
        response = self.requester.get(endpoint, params={"nested": nested})
        return self._extract_json(response)

    def get_all_assets(
        self,
        params: Optional[dict[str, Any]] = None,
        live: bool = False,
    ) -> List[Dict[str, Any]]:
        endpoint = self.endpoint.build("trade", "/v2/assets", live)
        response = self.requester.get(endpoint, params)
        return self._extract_json(response)

    def get_asset(self, symbol: str, live: bool = False) -> Dict[str, Any]:
        """
        Get asset information.

        Retrieves information about a specific asset based on its symbol.

        Args:
            symbol (str): The symbol of the asset (e.g., "AAPL").
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            Dict[str, Any]: Information about the asset, including details like name, exchange, and status.
        """
        endpoint = self.endpoint.build("trade", f"/v2/assets/{symbol}", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_all_positions(self, live: bool = False) -> List[Dict[str, float]]:
        endpoint = self.endpoint.build("trade", "/v2/positions", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_position(self, symbol: str, live: bool = False) -> Dict[str, Any]:
        # NOTE: # Raises a 422 Error if asset does not exist
        if "/" in symbol:
            products = symbol.split("/")
            symbol = "".join(products)
        endpoint = self.endpoint.build("trade", f"/v2/positions/{symbol}", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_current_asset_value(
        self, symbol: str, live: bool = False
    ) -> Dict[str, float]:
        """
        Get the current value of an asset.

        Retrieves the current value of an asset, including its current price, quantity held, and market value.

        Args:
            symbol (str): The symbol of the asset (e.g., "AAPL").
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            Dict[str, float]: Information about the asset's current value, including current_price, qty, and market_value.
        """
        if "/" in symbol:
            products = symbol.split("/")
            symbol = "".join(products)

        endpoint = self.endpoint.build("trade", "/v2/positions", live)
        response = self.requester.get(endpoint)
        positions = self._extract_json(response)

        for position in positions:
            if position["symbol"] == symbol:
                return {
                    "market_price": float(position["current_price"]),
                    "total_quantity": float(position["qty"]),
                    "current_value": float(position["market_value"]),
                }

        return {}

    def create_order(
        self,
        symbol: str,
        quantity: float,
        side: str,
        type_: str,
        time_in_force: str,
        live: bool = False,
    ) -> Dict:
        """
        Create an Order.

        Places a new order for the given account. An order request may be rejected if the account is not authorized for trading,
        or if the tradable balance is insufficient to fill the order.

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
        endpoint = self.endpoint.build("trade", "/v2/orders", live=live)

        # Execute the POST request
        response = self.requester.post(endpoint, json=payload)

        return self._extract_json(response)

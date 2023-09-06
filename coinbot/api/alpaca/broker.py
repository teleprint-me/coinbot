"""
coinbot/api/alpaca/broker.py
"""
from typing import Dict, Optional, Union

from coinbot.api.alpaca.auth import AlpacaAuth
from coinbot.api.alpaca.rest import AlpacaREST


class AlpacaBroker(AlpacaREST):
    """A class for interacting with the Alpaca Broker API."""

    def __init__(
        self,
        auth: Optional[AlpacaAuth] = None,
        rate_limit: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize an instance of AlpacaBroker.

        Args:
            auth (AlpacaAuth, optional): An instance of the AlpacaAuth class for authentication.
                If not provided, it will use defaults or authentication from the .env file.
            rate_limit (float, optional): The rate limit for API requests in seconds.
                Defaults to 200 API calls per minute for the free Basic plan.
            timeout (int, optional): Timeout value for HTTP requests in seconds.
                Defaults to 30 seconds.
        """
        super().__init__(auth, rate_limit, timeout)

    def get_clock(self, live: bool = True) -> Dict[str, Union[str, bool]]:
        """
        Get the market clock.

        The clock API serves the current market timestamp, whether or not the market is currently open,
        as well as the times of the next market open and close.

        Args:
            live (bool, optional): Whether to use live trading data. Default is True.

        Returns:
            Dict[str, Union[str, bool]]: A dictionary representing the market state.
                Keys are 'timestamp', 'is_open', 'next_open', and 'next_close'.
                'timestamp' is the current market timestamp.
                'is_open' is a boolean indicating whether the market is currently open.
                'next_open' is the timestamp of the next market open.
                'next_close' is the timestamp of the next market close.
        """
        endpoint = self.endpoint.build("broker", "/v2/clock", live)
        response = self.requester.get(endpoint)
        return self._extract_json(response)

    def get_amount_from_orders(self, symbol: str, live: bool = False) -> float:
        """
        Get the total quantity of a specified asset from closed and filled orders.

        Retrieves the total filled quantity of a specified asset from closed orders.

        Args:
            symbol (str): The symbol of the asset (e.g., "AAPL", "BTC/USD").
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            float: The total filled quantity of the asset from closed orders.
        """
        total_qty = 0.0
        endpoint = self.endpoint.build("broker", "/v2/orders", live=live)
        params = {
            "status": "closed",
            "symbol": symbol,
        }

        response = self.requester.get(endpoint, params=params)
        orders = self._extract_json(response)

        for order in orders:
            if order["symbol"] == symbol and order["status"] == "filled":
                total_qty += float(order["filled_qty"])

        return total_qty

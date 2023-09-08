"""
coinbot/api/alpaca/data.py
"""
from collections import defaultdict
from typing import Any, Dict, List, Optional

from coinbot.api.alpaca.auth import AlpacaAuth
from coinbot.api.alpaca.rest import AlpacaREST


class AlpacaMarketData(AlpacaREST):
    """A class for interacting with the Alpaca Market Data API."""

    def __init__(
        self,
        auth: Optional[AlpacaAuth] = None,
        rate_limit: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize an instance of AlpacaMarketData.

        Args:
            auth (AlpacaAuth, optional): An instance of the AlpacaAuth class for authentication.
                If not provided, it will use defaults or authentication from the .env file.
            rate_limit (float, optional): The rate limit for API requests in seconds.
                Defaults to 200 API calls per minute for the free Basic plan.
            timeout (int, optional): Timeout value for HTTP requests in seconds.
                Defaults to 30 seconds.
        """
        super().__init__(auth, rate_limit, timeout)

    def get_latest_crypto_quote(self, symbol: str, live: bool = False) -> float:
        """
        Get the latest crypto quote.

        Retrieves the last bid price (bp) for a specified crypto asset.

        Args:
            symbol (str): The symbol of the crypto asset (e.g., "BTC/USD").
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            float: The last bid price (bp) for the specified crypto asset.
        """
        endpoint = self.endpoint.build(
            "data",
            "/v1beta3/crypto/us/latest/quotes",
            live=live,
        )
        response = self.requester.get(endpoint, params={"symbols": symbol})
        data = self._extract_json(response)
        return float(data["quotes"][symbol]["bp"])

    def get_latest_stock_quote(
        self,
        symbol: str,
        feed: str = "sip",
        live: bool = False,
    ) -> float:
        """
        Get the latest stock quote.

        Retrieves the last bid price (bp) for a specified stock symbol.

        Args:
            symbol (str): The symbol of the stock (e.g., "AAPL").
            feed (str, optional): The market data feed. Defaults to "sip".
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            float: The last bid price (bp) for the specified stock symbol.
        """
        endpoint = self.endpoint.build("data", "/v2/stocks/quotes/latest", live)
        response = self.requester.get(
            endpoint, params={"symbols": symbol, "feed": feed}
        )
        data = self._extract_json(response)
        return float(data["quotes"]["quotes"][symbol]["bp"])

    def get_current_market_price(
        self,
        symbol: str,
        feed: str = "sip",
        asset_class: str = "stock",
        live: bool = False,
    ) -> float:
        """
        Get the current market price for an asset.

        Retrieves the current market price for a specified asset, which can be either a crypto or a stock.

        Args:
            symbol (str): The symbol of the asset (e.g., "BTC/USD" for crypto or "AAPL" for stock).
            feed (str, optional): The market data feed. Defaults to "sip" for stocks.
            asset_class (str, optional): The asset class ("crypto" or "stock"). Defaults to "stock".
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            float: The current market price for the specified asset.
        """
        if asset_class == "crypto":
            return self.get_latest_crypto_quote(symbol, live)
        elif asset_class == "stock":
            return self.get_latest_stock_quote(symbol, feed, live)
        else:
            raise ValueError(f"Unsupported asset class: {asset_class}")

    def get_crypto_candlesticks(
        self,
        loc: str,
        params: Dict[str, Any],
        live: bool = False,
    ) -> Dict[str, List[Dict]]:
        """
        Fetch historical crypto candlestick data from the Alpaca API.

        Args:
            loc (str): Crypto location, e.g., "us".
            params (dict[str, Any]): Parameters for the API request.
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            Dict[str, List[Dict]]: Historical candlestick data for specified symbols.
        """
        endpoint = self.endpoint.build("data", f"/v1beta3/crypto/{loc}/bars", live)
        response = self.requester.get(endpoint, params=params)
        json_data = self._extract_json(response)
        return json_data.get("bars", {})

    def page_crypto_candlesticks(
        self,
        loc: str,
        params: Dict[str, Any],
        live: bool = False,
    ) -> Dict[str, List[Dict]]:
        """
        Fetch paginated historical crypto candlestick data from the Alpaca API.

        Retrieves candlestick data for specified crypto assets, handling pagination if applicable.

        Args:
            loc (str): Crypto location, e.g., "us".
            params (Dict[str, Any]): Parameters for the API request.
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            Dict[str, List[Dict]]: Historical candlestick data for specified symbols, paginated if needed.
        """
        all_bars = defaultdict(list)
        endpoint = self.endpoint.build("data", f"/v1beta3/crypto/{loc}/bars", live=live)

        for response in self.requester.page(endpoint, params):
            json_data = self._extract_json(response)
            bars = json_data.get("bars", {})

            if not bars:
                break

            for asset_pair, asset_bars in bars.items():
                all_bars[asset_pair].extend(asset_bars)

        return dict(all_bars)

"""
coinbot/api/alpaca/endpoint.py
"""


class AlpacaEndpoint:
    """A utility class for constructing Alpaca API endpoints."""

    def __init__(self):
        """
        Initialize an instance of AlpacaEndpoint.

        Defines the Alpaca API sub-domains based on context.
        """
        self.ALPACA_SUBDOMAINS = {
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

    def _normalize_url(self, endpoint: str) -> str:
        """
        Normalize the endpoint by adding a leading slash if missing.

        Args:
            endpoint (str): The endpoint to normalize.

        Returns:
            str: The normalized endpoint.
        """
        return endpoint if endpoint.startswith("/") else "/" + endpoint

    def _get_api_url(self, subdomain: str, context: str, endpoint: str) -> str:
        """
        Construct the Alpaca API URL based on sub-domain, context, and endpoint.

        Args:
            subdomain (str): The API sub-domain ("broker", "trade", or "data").
            context (str): The context ("paper" for paper trading, "live" for live trading).
            endpoint (str): The specific endpoint to access.

        Returns:
            str: The full API URL based on the provided parameters.

        Example:
            trade_api_url = self._get_api_url("trade", "live", "/v2/orders")
            print(trade_api_url)
        """
        normalized_endpoint = self._normalize_url(endpoint)
        return f"{self.ALPACA_SUBDOMAINS[subdomain][context]}{normalized_endpoint}"

    def build(self, subdomain: str, endpoint: str, live: bool = False) -> str:
        """
        Constructs the Alpaca API endpoint based on sub-domain and live flag.

        Args:
            subdomain (str): The API sub-domain ("broker", "trade", or "data").
            endpoint (str): The specific endpoint to access.
            live (bool, optional): Whether to use live trading data. Default is False.

        Returns:
            str: The constructed API endpoint.
        """
        context = "live" if live else "paper"
        return self._get_api_url(subdomain, context, endpoint)

"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.advanced
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
@ref https://docs.cdp.coinbase.com/coinbase-app/trade/reference
"""

from typing import Iterator, Optional

from coinbot.coinbase.client import Client, Subscriber


class Account(Subscriber):
    def list(self, params: Optional[dict] = None) -> Iterator[dict]:
        """
        List accounts with optional pagination parameters.

        :param params: Query parameters for pagination.
            - limit (int): The number of accounts to return per page.
            - cursor (str): The cursor for pagination.
        :return: A dictionary containing the list of accounts.
        """
        return self.client.paginate("accounts", key="accounts", params=params)

    def get(self, account_uuid: str) -> dict:
        """
        Retrieve details of a specific account by its UUID.

        :param account_uuid: The UUID of the account.
        :return: A dictionary containing the account details.
        """
        return self.client.get(f"accounts/{account_uuid}").json()


class Order(Subscriber):
    def cancel(self, *, order_ids: list[str]) -> dict:
        """
        Cancel one or more orders by UUID.

        :param order_ids: List of order UUIDs to cancel.
        :return: Dictionary containing success/failure results per ID.
        """
        if not order_ids:
            raise ValueError("Must provide at least one order ID.")
        return self.client.post(
            "orders/batch_cancel", data={"order_ids": order_ids}
        ).json()

    def create(self, params: dict) -> dict:
        """
        Create a new order.

        :param params: Dictionary containing order parameters:
            - client_order_id (str): Unique identifier for the order.
            - product_id (str): Asset-pair identifier (e.g., BTC-USD).
            - side (str): Side of the order (buy/sell).
            - order_configuration (dict): Configuration of the order (type, size, etc.)
                - market_market_ioc (dict): Market market IOC order configuration.
                    - quote_size (str): Quote size for the order.
                    - base_size (str): Base size for the order.
                    - rfq_disabled (bool): Routed to CLOB exchange if True.
            - Reference docs for limit order details (See module docstring).
        :return: Dictionary containing the created order details.
        """
        required = ("client_order_id", "product_id", "side", "order_configuration")
        for key in required:
            if key not in params:
                raise ValueError(f"Missing required parameter: '{key}'")
        return self.client.post("orders", data=params).json()

    def get(self, order_id: str) -> dict:
        """
        Retrieve historical order details by ID.

        Note: Params are deprecated and will be removed in future versions.

        :param order_id: Order UUID.
        :return: Dictionary containing order details.
        """
        return self.client.get(f"orders/historical/{order_id}").json()

    def fills(self, params: Optional[dict] = None) -> Iterator[dict]:
        """
        Fetch historical fills with optional filters.

        :param params: Optional filters:
            - order_ids (list[str]): Filter by specific order UUIDs.
            - trade_ids (list[str]): Filter by trade UUIDs.
            - product_ids (list[str]): Filter by product pairs.
            - start_sequence_timestamp (str): Start time (RFC 3339).
            - end_sequence_timestamp (str): End time (RFC 3339).
            - limit (int): Max number of fills.
            - cursor (str): Pagination cursor.
            - sort_by (str): Sort key (e.g., "trade_time").
        :return: Dictionary containing list of fills.
        """
        return self.client.paginate(
            "orders/historical/fills", key="fills", params=params
        )

    def list(self, params: Optional[dict] = None) -> Iterator[dict]:
        """
        List all historical orders with optional filters.

        :param params: Optional filters:
            - order_ids (list[str]): Filter by specific order UUIDs.
            - product_ids (list[str]): Filter by product pairs.
            - product_type (str): Filter by order type (e.g "spot", "future").
            - order_status (list[str]): Filter by order status.
            - order_types (list[str]): Filter by order types (e.g. "market").
            - order_side (str): Filter by order side (e.g. "buy", "sell").
            - start_date (str): Start date (RFC 3339).
            - end_date (str): End date (RFC 3339).
            - limit (int): Maximum number of orders to return.
            - cursor (str): Cursor for pagination.
            - sort_by (str): Sort by (e.g. "limit_price", "last_fill_time").
        :return: Dictionary containing order data.
        """
        return self.client.paginate(
            "orders/historical/batch", key="orders", params=params
        )


class Product(Subscriber):
    def best_bid_ask(self, product_ids: list[str]) -> dict:
        """
        Retrieve best bid/ask for one or more products.

        :param params: Query parameters:
            - product_ids (list[str]): List of product IDs (e.g., BTC-USD,ETH-USD).
        :return: Dictionary with best bid/ask prices keyed by product_id.
        """
        if not product_ids:
            raise ValueError("Must provide at least one product ID.")
        return self.client.get(
            "best_bid_ask", params={"product_ids": product_ids}
        ).json()

    def ticker(self, product_id: str, params: dict) -> dict:
        """
        Retrieve recent trade price summary for a product.

        :param product_id: The trading pair (e.g., BTC-USD).
        :param params: Query parameters:
            - limit (int): Required. Number of trades to aggregate (1-100).
            - start (str): Optional. Start timestamp in ISO 8601.
            - end (str): Optional. End timestamp in ISO 8601.
        :return: Dictionary with OHLC and trade data.
        """
        if "limit" not in params:
            raise ValueError("Missing required parameter: 'limit'")
        return self.client.get(f"products/{product_id}/ticker", params=params).json()

    def get(self, product_id: str) -> dict:
        """
        Get metadata and market config for a product.

        :param product_id: The trading pair (e.g., BTC-USD).
        :return: Dictionary describing product config.
        """
        return self.client.get(f"products/{product_id}").json()

    def book(self, params: dict) -> dict:
        """
        Retrieve the current order book for a product.

        :param params: Query parameters:
            - product_id (str): Required. The product ID (e.g., BTC-USD).
            - limit (int): Optional. Number of levels to return (1-100).
            - aggregation_price_increment (str): Optional. e.g., "0.01"
        :return: Dictionary with bids, asks, and metadata.
        """
        if "product_id" not in params:
            raise ValueError("Missing required parameter: 'product_id'")
        return self.client.get("product_book", params=params).json()

    def candles(self, product_id: str, params: dict) -> list:
        """
        Retrieve historical OHLC data for a product.

        :param product_id: The trading pair (e.g., BTC-USD).
        :param params: Query parameters:
            - start (str): Required. ISO 8601 start timestamp.
            - end (str): Required. ISO 8601 end timestamp.
            - granularity (int): Required. Seconds between candle buckets.
            - limit (int): Optional. Max number of candles to return (default: 300).
        :return: List of candles, each as [start, low, high, open, close, volume].
        """
        for key in ("start", "end", "granularity"):
            if key not in params:
                raise ValueError(f"Missing required parameter: '{key}'")
        return self.client.get(f"products/{product_id}/candles", params=params).json()

    def list(self, params: Optional[dict] = None) -> list:
        """
        List all available trading products.

        :param params: Optional query parameters:
            - limit (int): Max number of products to return.
            - offset (int): Offset for pagination.
            - product_type (str): Optional. (e.g., SPOT).
            - product_ids (list[str]): List of product IDs (e.g., BTC-USD,ETH-USD).
            - product_sort_order (str): asc or desc.
        :return: List of product metadata.
        """
        return self.client.get("products", params=params).json()


class CoinbaseAdvanced:
    def __init__(self, client: Client):
        self.client = client
        self.account = Account(client)
        self.order = Order(client)
        self.product = Product(client)

    def __repr__(self) -> str:
        return f"CoinbaseAdvanced(key={self.key})"

    def __str__(self) -> str:
        return " ".join(word.capitalize() for word in self.name.split("_"))

    @property
    def key(self) -> str:
        return self.client.auth.api.key

    @property
    def name(self):
        return "coinbase_advanced"

    def plug(self, cls: object, name: str):
        instance = cls(self.client)
        setattr(self, name, instance)


if __name__ == "__main__":
    import json
    import os

    from dotenv import load_dotenv

    from coinbot.coinbase.client import API, Auth, Client

    load_dotenv(".env")

    api = API(
        settings={
            "key": os.getenv("COINBASE_API_KEY"),
            "secret": os.getenv("COINBASE_API_SECRET"),
            "version": 3,
        }
    )

    client = Client(api, Auth(api))
    advanced = CoinbaseAdvanced(client)

    for item in advanced.order.fills({"limit": 5, "product_ids": ["BTC-USD"]}):
        print(json.dumps(item, indent=2))

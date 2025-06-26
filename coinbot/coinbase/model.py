"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.model
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
@ref https://docs.cdp.coinbase.com/coinbase-app/trade/reference
"""

from typing import Optional

from coinbot.coinbase.client import Client, Subscriber


class Account(Subscriber):
    def list(self, params: Optional[dict] = None) -> dict:
        """
        List accounts with optional pagination parameters.

        :param params: Dictionary of parameters for pagination.
                      - limit (int): The number of accounts to return per page.
                      - cursor (str): The cursor for pagination.
        :return: A dictionary containing the list of accounts.
        """
        return self.client.get("accounts", params=params).json()

    def get(self, account_uuid: str) -> dict:
        """
        Retrieve details of a specific account by its UUID.

        :param account_uuid: The UUID of the account.
        :return: A dictionary containing the account details.
        """
        return self.client.get(f"accounts/{account_uuid}").json()


class Product(Subscriber):
    def best_bid_ask(self, params: dict) -> dict:
        """
        Retrieve the best bid and ask prices for a product.

        :param params: Dictionary of parameters for the request.
                      - product_ids (str): The list of trading pairs.
        :return: A dictionary containing the best bid and ask prices.
        """
        return self.client.get(f"best_bid_ask", params=params).json()

    def ticker(self, product_id: str, params: dict) -> dict:
        """
        Retrieve the ticker data for a product.

        :param product_id: The trading pair.
        :param params: Dictionary of parameters for the request.
                      - limit (int, required): The number of recent trades to return.
                      - start (str): The UNIX timestamp indicating the start of the time interval.
                      - end (str): The UNIX timestamp indicating the end of the time interval.
        :return: A dictionary containing the ticker.
        """
        return self.client.get(f"products/{product_id}/ticker", params).json()

    def get(self, product_id: str) -> dict:
        """
        Retrieve the product details for a product.

        :param product_id: The trading pair.
        :return: A dictionary containing the product details.
        """
        return self.client.get(f"products/{product_id}").json()

    def book(self, params: dict) -> dict:
        """
        Retrieve the order book for a product.

        :param params: Dictionary of parameters for the request.
                      - product_id (str, required): The trading pair.
                      - limit (int): The number of bids and asks to return.
                      - aggregation_price_increment (str): Minimum price intervals for grouping bids and asks.
        :return: A dictionary containing the order book.
        """
        return self.client.get(f"product_book", params).json()

    def candles(self, product_id: str, params: dict) -> list:
        """
        Retrieve the historical price data for a product.

        :param product_id: The trading pair.
        :param params: Dictionary of parameters for the request.
                      - start (str, required): The start time of the data.
                      - end (str, required): The end time of the data.
                      - granularity (int, required): The time interval for the data.
                      - limit (int): The maximum number of candles to return.
        :return: A list of dictionaries containing the historical price data.
        """
        return self.client.get(f"products/{product_id}/candles", params).json()

    def list(self, params: Optional[dict] = None) -> list:
        """
        Retrieve a list of all products.

        :param params: Dictionary of parameters for the request.
                      - limit (int): The maximum number of products to return.
                      - offset (int): Number of products to skip before returning.
                      - product_type (str): The type of products to return.
                      - product_sort_order (str): The order in which to return the products.
        :return: A list of dictionaries containing the list of products.
        """
        return self.client.get("products", params).json()


class CoinbaseAdvanced:
    def __init__(self, client: Client):
        self.client = client
        self.account = Account(client)
        # self.order = Order(client)
        self.product = Product(client)
        # Plug in more endpoints as you formalize them

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
    account = Account(client)

    all_accounts = account.list({"limit": 5})
    print(json.dumps(all_accounts, indent=2))

    first_uuid = all_accounts["accounts"][0]["uuid"]
    single_account = account.get(first_uuid)
    print(json.dumps(single_account, indent=2))

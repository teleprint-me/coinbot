"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.model
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
@ref https://docs.cdp.coinbase.com/coinbase-app/trade/reference
"""

from coinbot.coinbase.client import Client, Subscriber


class Account(Subscriber):
    def list(self, params: dict) -> dict:
        return self.client.get("accounts", params=params).json()

    def get(self, account_uuid: str) -> dict:
        return self.client.get(f"accounts/{account_uuid}").json()


class Product(Subscriber):
    def best_bid_ask(self, params: dict) -> dict:
        return self.client.get(f"best_bid_ask", params=params).json()

    def ticker(self, product_id: str) -> dict:
        return self.client.get(f"products/{product_id}/ticker").json()

    def list(self):
        return self.client.get("products").json()

    def get(self, product_id: str) -> dict:
        return self.client.get(f"products/{product_id}").json()

    def book(self, product_id: str, data: dict = None) -> dict:
        return self.client.get(f"products/{product_id}/book", data).json()

    def trades(self, product_id: str, data: dict = None) -> list:
        return self.client.get(f"products/{product_id}/trades", data).json()

    def candles(self, product_id: str, data: dict = None) -> list:
        return self.client.get(f"products/{product_id}/candles", data).json()

    def stats(self, product_id: str) -> dict:
        return self.client.get(f"products/{product_id}/stats").json()


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

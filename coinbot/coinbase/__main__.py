"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.__main__
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
"""

import os

import dotenv

from coinbot.coinbase.client import API, Auth, Client

if not dotenv.load_dotenv(".env"):
    raise ValueError("Failed to read dotenv")

if __name__ == "__main__":
    api = API(
        settings={
            "key": os.getenv("COINBASE_API_KEY"),
            "secret": os.getenv("COINBASE_API_SECRET"),
            "version": 3,
        }
    )

    auth = Auth(api)
    client = Client(api, auth)

    # Example: get product data
    resp = client.get("products/BTC-USD")
    print(resp.json())

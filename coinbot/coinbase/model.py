"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.model
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
"""

from typing import Optional

from coinbot.coinbase.client import Client, Subscriber


class Account(Subscriber):
    def list(self, limit: int = 10, cursor: Optional[str] = None) -> dict:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        return self.client.get("accounts", params=params).json()

    def get(self, account_uuid: str) -> dict:
        return self.client.get(f"accounts/{account_uuid}").json()


if __name__ == "__main__":
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

    all_accounts = account.list()
    print(all_accounts)

    first_uuid = all_accounts["accounts"][0]["uuid"]
    single_account = account.get(first_uuid)
    print(single_account)

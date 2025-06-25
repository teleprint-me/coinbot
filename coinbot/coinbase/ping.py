import os

import dotenv

from coinbot.coinbase.api import API
from coinbot.coinbase.auth import Auth
from coinbot.coinbase.client import Client

if not dotenv.load_dotenv(".env"):
    raise ValueError("Failed to read dotenv")

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

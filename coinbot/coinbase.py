"""
coinbot/coinbase.py
"""

import logging
import os
from datetime import datetime

import dotenv
import requests
from cdp.auth.utils.jwt import JwtOptions, generate_jwt

if __name__ == "__main__":
    logger = logging.getLogger("coinbase")
    logger.setLevel(logging.DEBUG)

    dotenv.load_dotenv(".env")

    # Load secrets
    api_key = os.getenv("COINBASE_API_KEY")
    api_secret = os.getenv("COINBASE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("Missing api key and or secret")

    logger.debug(f"Loaded API Key: {bool(api_key)}")
    logger.debug(f"Loaded API Secret: {bool(api_secret)}")

    # Construct JWT
    jwt_token = generate_jwt(
        JwtOptions(
            api_key_id=api_key,
            api_key_secret=api_secret,
            request_method="GET",
            request_host="api.coinbase.com",  # no https:// here
            request_path="/api/v3/brokerage/products/BTC-USD/candles",
            expires_in=30,
        )
    )

    # Build query
    params = {
        "start": int(datetime(2020, 1, 1, 0, 0).timestamp()),
        "end": int(datetime(2020, 1, 1, 23, 59).timestamp()),
        "granularity": "ONE_HOUR",
    }

    # Request data
    response = requests.get(
        "https://api.coinbase.com/api/v3/brokerage/products/BTC-USD/candles",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        params=params,
    )

    # Output
    if response.status_code == 200:
        logger.info(response.json())
    else:
        logger.error(f"[ERROR] {response.status_code}: {response.content}")

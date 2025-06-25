"""
coinbot/coinbase.py
"""

import logging
import os
from datetime import datetime
from typing import Optional

import dotenv
import requests
from cdp.auth.utils.jwt import JwtOptions, generate_jwt

from coinbot import __agent__, __source__, __version__

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__host__ = "api.coinbase.com"
__timeout__ = 30
__limit__ = 1 / (36000 / 3600)


class Auth:
    def __init__(self, path: str = ".env"):
        if not dotenv.load_dotenv(path):
            raise ValueError("Failed to load .env")

        self.key = os.getenv("COINBASE_API_KEY", "").strip()
        self.secret = os.getenv("COINBASE_API_SECRET", "").strip()

        if not self.key or not self.secret:
            raise ValueError("Missing api key and or secret")

        logger.debug(f"Loaded API Key: {bool(self.key)}")
        logger.debug(f"Loaded API Secret: {bool(self.secret)}")

    def __call__(self, method: str, path: str, timeout: int = __timeout__) -> dict:
        token = generate_jwt(
            JwtOptions(
                api_key_id=self.key,
                api_key_secret=self.secret,
                request_method=method,
                request_host=__host__,
                request_path=path,
                expires_in=timeout,
            )
        )
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }


class REST:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.session = requests.Session()

    def url(self, path: str) -> str:
        return f"https://{__host__}{path}"

    def get(self, path: str, params: dict = None, timeout: int = __timeout__) -> dict:
        response = self.session.get(
            self.url(path),
            headers=self.auth("GET", path, timeout),
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: dict = None, timeout: int = __timeout__) -> dict:
        response = self.session.post(
            self.url(path),
            headers=self.auth("POST", path, timeout),
            json=data,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    logger = logging.getLogger("coinbase")
    logger.setLevel(logging.DEBUG)

    # Build query
    params = {
        "start": int(datetime(2020, 1, 1, 0, 0).timestamp()),
        "end": int(datetime(2020, 1, 1, 23, 59).timestamp()),
        "granularity": "ONE_HOUR",
    }

    # Request data
    path = "/api/v3/brokerage/products/BTC-USD/candles"
    rest = REST(Auth())
    response = rest.get(path, params=params)

    # Output
    logger.info(response)

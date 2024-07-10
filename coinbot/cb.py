"""
coinbot/cb.py
"""
import hashlib
import hmac
import http.client
import logging
import os
import time
from datetime import datetime
from typing import Optional, Tuple

import dotenv
import requests
from requests.auth import AuthBase

# Initialize Logging
logging.basicConfig(level=logging.DEBUG)


def get_api_key(path: Optional[str] = ".env") -> Tuple[str, str]:
    # Try to load the .env file
    dotenv.load_dotenv(path)

    # Determine which keys to use, preferring Private over Public
    api_key = os.getenv("COINBASE_API_KEY")
    api_secret = os.getenv("COINBASE_API_SECRET")

    logging.debug(f"Loaded API Key: {bool(api_key)}")
    logging.debug(f"Loaded API Secret: {bool(api_secret)}")

    return api_key, api_secret


# Common Variables
api_key, api_secret = get_api_key()
timestamp = str(int(time.time()))
method = "GET"
path = "/v3/brokerage/products/BTC-USD/candles"
start = int((datetime(2020, 1, 1, 0, 0, 0) - datetime(1970, 1, 1)).total_seconds())
end = int((datetime(2020, 1, 1, 23, 59, 59) - datetime(1970, 1, 1)).total_seconds())
params = f"start={start}&end={end}&granularity=ONE_HOUR"
message = timestamp + method + path + ""
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Message: {message}")


# HTTP.client Method
def http_client_method():
    signature = hmac.new(
        api_secret.encode("utf-8"),
        message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    conn = http.client.HTTPSConnection("api.coinbase.com")
    headers = {
        "CB-ACCESS-KEY": api_key,
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-VERSION": "2022-10-17",
    }
    conn.request(method, path + f"?{params}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    logging.info(f"HTTP.client Response: {data}")


# Requests Method
class Auth(AuthBase):
    def __call__(self, request):
        signature = hmac.new(
            api_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        request.headers.update(
            {
                "CB-ACCESS-KEY": api_key,
                "CB-ACCESS-SIGN": signature,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-VERSION": "2022-10-17",
            }
        )
        return request


def requests_method():
    url = "https://api.coinbase.com" + path
    auth = Auth()
    response = requests.get(url, params=params, auth=auth)
    if response.status_code == 200:
        print("Requests Response:", response.json())
    else:
        logging.error(f"Failed to get data: {response.content}")


# Main Execution
if __name__ == "__main__":
    logging.debug(
        f"API Key Loaded: {api_key is not None}, API Secret Loaded: {api_secret is not None}"
    )

    http_client_method()
    requests_method()

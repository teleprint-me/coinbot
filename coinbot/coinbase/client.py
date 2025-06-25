import time

import requests
from requests import Response

from coinbot.coinbase.api import API
from coinbot.coinbase.auth import Auth


class Client:
    def __init__(self, api: API, auth: Auth):
        self.api = api
        self.auth = auth
        self.session = requests.Session()
        self.timeout = 30
        self.rate_limit = 1 / (36000 / 3600)  # ~0.1s per request

    def _request(self, method: str, path: str, data=None, params=None) -> Response:
        time.sleep(self.rate_limit)
        url = self.api.url(path)
        headers = self.auth.header(method, self.api.path(path), self.timeout)

        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=data,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def get(self, path: str, params=None) -> Response:
        return self._request("GET", path, params=params)

    def post(self, path: str, data=None) -> Response:
        return self._request("POST", path, data=data)

    def close(self) -> None:
        self.session.close()

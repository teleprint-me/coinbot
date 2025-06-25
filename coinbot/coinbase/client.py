"""
Copyright (C) 2021 - 2025 Austin Berrio
@file coinbot.coinbase.api
@brief A Python API Adapter for Coinbase Advanced
@license AGPL
"""

import logging
import time
from dataclasses import dataclass, field

import requests
from cdp.auth.utils.jwt import JwtOptions, generate_jwt
from requests import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class API:
    settings: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return self.settings.get("key", "")

    @property
    def secret(self) -> str:
        return self.settings.get("secret", "")

    @property
    def version(self) -> int:
        return self.settings.get("version", 3)

    @property
    def rest(self) -> str:
        return self.settings.get("rest", "https://api.coinbase.com")

    def path(self, value: str) -> str:
        return f"/api/v{self.version}/brokerage/{value.lstrip('/')}"

    def url(self, value: str) -> str:
        return f"{self.rest}{self.path(value)}"


class Auth:
    def __init__(self, api: API):
        self.api = api

    def header(self, method: str, path: str, timeout: int = 30) -> dict[str, str]:
        token = generate_jwt(
            JwtOptions(
                api_key_id=self.api.key,
                api_key_secret=self.api.secret,
                request_method=method,
                request_host="api.coinbase.com",
                request_path=path,
                expires_in=timeout,
            )
        )
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }


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


class Subscriber:
    def __init__(self, client: Client = None):
        self.__client = client if client else Client()

    @property
    def client(self) -> Client:
        return self.__client

    # NOTE: error is left here as a convenience method for plugs
    def error(self, response: Response) -> bool:
        return 200 != response.status_code

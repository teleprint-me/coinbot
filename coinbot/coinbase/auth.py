import logging

from cdp.auth.utils.jwt import JwtOptions, generate_jwt

from coinbot.coinbase.api import API

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Auth:
    def __init__(self, api: API):
        self.api = api

    def header(self, method: str, path: str, timeout: int = 30) -> dict:
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

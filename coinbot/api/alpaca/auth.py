"""
coinbot/api/alpaca/auth.py

usage:
    # Create an instance of AlpacaAuth with API keys loaded from a .env file
    # NOTE: This is preferred for security purposes.
    auth = AlpacaAuth(path=".env")

    # Alternatively, provide API keys explicitly
    # NOTE: This is discouraged for security purposes.
    auth = AlpacaAuth(key="your_api_key_here", secret="your_api_secret_here")

    # Access the API key and secret for further use
    api_key = auth.key
    api_secret = auth.secret
"""
import base64
import os
from typing import Optional
from urllib.parse import urlparse

import dotenv
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbot import __agent__, __source__, __version__, logging


class AlpacaAuth(AuthBase):
    """Create and return an HTTP request with authentication headers."""

    def __init__(
        self,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        path: Optional[str] = None,
    ):
        """
        Initialize an instance of the AlpacaAuth class with API credentials.

        Args:
            key (str, optional): The Alpaca API key. If not provided, it will be
                retrieved from environment variables.
            secret (str, optional): The Alpaca API secret key. If not provided, it
                will be retrieved from environment variables.
            path (str, optional): The path to the .env file containing API credentials.
        """
        # Try to load environment variables from the .env file
        if not key and not secret:
            env_loaded = dotenv.load_dotenv(path)
        else:
            env_loaded = False

        # Assign API keys and secrets
        # Priority: Environment variables (Paper over Live) > Constructor arguments > Empty string
        if env_loaded:
            self.key = (
                os.getenv("PAPER_ALPACA_API_KEY") or os.getenv("ALPACA_API_KEY") or ""
            )
            self.secret = (
                os.getenv("PAPER_ALPACA_API_SECRET")
                or os.getenv("ALPACA_API_SECRET")
                or ""
            )
        elif key is not None and secret is not None:
            self.key = key
            self.secret = secret
        else:
            # Fallback to empty strings if no other options are available
            self.key = ""
            self.secret = ""

        # Log if environment variables couldn't be loaded
        if not env_loaded:
            logging.warning(
                "Could not load environment variables. Falling back to provided keys or public endpoints."
            )

        # Log the status of keys and secrets
        if self.key and self.secret:
            # Mask the last 4 characters of both the key and the secret for security
            logging.debug(f"Alpaca API Key: ****{self.key[-4:]}")
            logging.debug(f"Alpaca API Secret: ****{self.secret[-4:]}")
        elif not self.key or not self.secret:
            # Log an error if either the key or secret is missing, suggesting a likely user error
            logging.error(
                "Either Key or Secret is missing. "
                "Revise your source code and environment variables to ensure both are passed as arguments."
            )
        else:
            # Log a warning if both the key and secret are missing
            logging.warning(
                "Key and Secret are missing. Fallback to public endpoints with limited access."
            )

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """
        Return the prepared request with updated headers.

        Args:
            request (PreparedRequest): A prepared HTTP request.

        Returns:
            PreparedRequest: The same request with updated headers.
        """
        header = {}
        parsed_url = urlparse(request.url)
        sub_domain = parsed_url.netloc.split(".")[0]

        logging.debug(f"Auth Url: {request.url}")
        logging.debug(f"Auth Path: {request.path_url}")

        # Define common headers that are shared across all API versions and types
        common_headers = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Define default headers for most subdomains, including authentication keys
        default_headers = {
            **common_headers,
            "APCA-API-KEY-ID": self.key,
            "APCA-API-SECRET-KEY": self.secret,
        }

        # Create a dictionary that maps subdomains to their respective headers
        # "broker-api" requires special handling with Basic Authorization
        header_configs = {
            "broker-api": {
                **common_headers,
                "Authorization": f"Basic {base64.b64encode(f'{self.key}:{self.secret}'.encode('utf-8')).decode('utf-8')}",
            },
            "api": default_headers,
            "paper-api": default_headers,
            "data": default_headers,
        }

        # Retrieve the appropriate headers for the subdomain or use default headers
        header = header_configs.get(sub_domain, default_headers)

        # Log censored information if debug is enabled
        censored_header = {
            k: "****" + v[-4:]
            if "KEY" in k or "SECRET" in k or "Authorization" in k
            else v
            for k, v in header.items()
        }
        logging.debug(f"Censored Alpaca Header: {censored_header}")

        # Inject payload
        request.headers.update(header)

        return request

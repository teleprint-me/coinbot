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
import os
from typing import Dict, Optional

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
        # Sign and authenticate payload.
        header: Dict = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "APCA-API-KEY-ID": self.key,
            "APCA-API-SECRET-KEY": self.secret,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Censor sensitive information for debugging
        censored_header: Dict = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "APCA-API-KEY-ID": f"****{self.key[-4:]}",
            "APCA-API-SECRET-KEY": f"****{self.secret[-4:]}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Log censored information if debug is enabled
        logging.debug(f"Censored Alpaca Header: {censored_header}")

        # Inject payload
        request.headers.update(header)

        return request

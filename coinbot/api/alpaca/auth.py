"""
coinbot/api/alpaca/auth.py
"""
import os
from typing import Dict

import dotenv
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbot import __agent__, __source__, __version__, logging


class AlpacaAuth(AuthBase):
    """
    Create and return an HTTP request with authentication headers.

    Args:
        path (str): The path to the .env file containing API credentials.
            If not provided, the default is ".env".
    """

    def __init__(self, path: str = ".env"):
        """
        Create an instance of the AlpacaAuth class.

        Args:
            path (str): The path to the .env file containing API credentials.
                If not provided, the default is ".env".
        """
        # Try to load the .env file
        env_loaded = dotenv.load_dotenv(path)

        if not env_loaded:
            # Log a warning but continue execution
            print(f"Warning: Failed to load {path}")

        # Determine which keys to use, preferring Paper over Live
        self.key = (
            os.getenv("PAPER_ALPACA_API_KEY") or os.getenv("ALPACA_API_KEY") or ""
        )
        self.secret = (
            os.getenv("PAPER_ALPACA_API_SECRET") or os.getenv("ALPACA_API_SECRET") or ""
        )

        if not self.key or not self.secret:
            logging.warning(
                "An issue with Key and/or Secret was detected. "
                "Some functionalities may be restricted."
            )

        logging.debug(f"Alpaca API Key: ****{self.key[-4:]}")
        logging.debug(f"Alpaca API Secret: ****{self.secret[-4:]}")

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

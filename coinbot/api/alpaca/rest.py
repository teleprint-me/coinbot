"""
coinbot/api/alpaca/rest.py
"""
from json import JSONDecodeError
from typing import Any, Dict, Optional, Protocol

from requests import RequestException, Response

from coinbot import logging
from coinbot.api.alpaca.auth import AlpacaAuth
from coinbot.api.alpaca.endpoint import AlpacaEndpoint
from coinbot.api.alpaca.request import AlpacaRequest


class AlpacaREST(Protocol):
    """A Base class for interacting with the Alpaca REST API."""

    def __init__(
        self,
        auth: Optional[AlpacaAuth] = None,
        rate_limit: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize an instance of AlpacaREST.

        Args:
            auth (AlpacaAuth, optional): An instance of the AlpacaAuth class for authentication.
                If not provided, it will use defaults or authentication from the .env file.
            rate_limit (float, optional): The rate limit for API requests in seconds.
                Defaults to 200 API calls per minute for the free Basic plan.
            timeout (int, optional): Timeout value for HTTP requests in seconds.
                Defaults to 30 seconds.

        Attributes:
            endpoint (AlpacaEndpoint): An instance of the AlpacaEndpoint for constructing API endpoints.
            requester (AlpacaRequest): An instance of the AlpacaRequest for making HTTP requests.
        """
        self.endpoint = AlpacaEndpoint()
        self.requester = AlpacaRequest(auth, rate_limit, timeout)

    def _extract_json(self, response: Response) -> Dict[str, Any]:
        """
        Extract and parse JSON data from an HTTP response.

        Args:
            response (Response): The HTTP response object.

        Returns:
            Dict[str, Any]: A dictionary representing the parsed JSON data.

        Raises:
            RequestException: If there is an error in parsing or if the response status code is not 200.
        """
        try:
            json_data = response.json()

            # NOTE: Alpaca has useful error messages that are easily amalgamated.
            if response.status_code != 200:
                error_message = json_data.get("message", "Unknown error")
                raise RequestException(
                    f"Error ({response.status_code}): {error_message}"
                )

            return json_data

        except JSONDecodeError as message:
            logging.error(message)
            raise RequestException(f"Error ({response.status_code}): {response.text}")

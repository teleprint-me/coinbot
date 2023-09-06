"""
coinbot/api/alpaca/request.py
"""
from json import JSONDecodeError
from time import sleep
from typing import Dict, Generator, Optional

import requests
from requests import RequestException, Response

from coinbot import logging
from coinbot.api.alpaca.auth import AlpacaAuth


class AlpacaRequest:
    """A class for making HTTP requests to the Alpaca API."""

    def __init__(
        self,
        auth: Optional[AlpacaAuth] = None,
        rate_limit: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize an instance of AlpacaRequest.

        Args:
            auth (AlpacaAuth, optional): An Alpaca authentication object.
                If not provided, it will use defaults from a ".env" file.
            rate_limit (float, optional): The rate limit for API requests in seconds.
                Defaults to 200 API calls per minute for the free Basic plan.
            timeout (int, optional): Timeout value for HTTP requests in seconds.
                Defaults to 30 seconds.
        """
        # NOTE: Use sane defaults for authentication if None are provided
        self.__auth = auth or AlpacaAuth(".env")
        # NOTE: Rate limit of API requests in seconds.
        # Plus is $99/mo and allows 10,000 API calls/min
        # Basic is free and allows 200 API calls/min
        self.__limit = rate_limit or 1 / (200 / 60)  # Default to 200 calls/min
        # NOTE: Timeout value for HTTP requests.
        self.__timeout = timeout or 30  # Default to 30s timeout

    def _request(self, method, url, **kwargs) -> Response:
        """
        Send an HTTP request to the specified URL with the given method.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Response: The response object from the HTTP request.

        Raises:
            RequestException: If there is an error in making the HTTP request.
        """
        sleep(self.__limit)

        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.__auth,
                timeout=self.__timeout,
                **kwargs,
            )
            return response
        except RequestException as error:
            raise RequestException(error)

    def get(self, url: str, params: Optional[Dict] = None) -> Response:
        """
        Perform a GET request to the specified API path.

        Args:
            url (str): The API endpoint to be requested.
            params (dict, optional): Query parameters to be passed with the request.

        Returns:
            Response: The response of the GET request.
        """
        return self._request("GET", url, params=params)

    def post(self, url: str, json: Optional[Dict] = None) -> Response:
        """
        Perform a POST request to the specified API path.

        Args:
            path: The API endpoint to be requested.
            json: (optional) JSON payload to be sent with the request.

        Returns:
            Response: The response of the POST request.
        """
        return self._request("POST", url, json=json)

    def page(
        self, url: str, params: Optional[Dict] = None
    ) -> Generator[Response, None, None]:
        """
        Pages through API responses.

        Args:
            url (str): API endpoint URL.
            params (Optional[Dict]): Query parameters for the API call.

        Yields:
            Response: HTTP Response object for each page.
        """
        next_page_token = None  # Initialize the page token

        while True:
            if next_page_token is not None:
                params = params or {}
                params["page_token"] = next_page_token

            # Perform a GET request to the specified API path.
            response = self.get(url, params=params)
            yield response

            try:
                json_data = response.json()
                next_page_token = json_data.get("next_page_token")
            except JSONDecodeError as message:
                logging.error(message)
                raise RequestException(f"Error {response.status_code}: {response.text}")

            if next_page_token is None:
                break

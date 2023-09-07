"""
tests/alpaca/test_alpaca_request.py
"""
import pytest
from requests.exceptions import RequestException

from coinbot.api.alpaca import AlpacaAuth, AlpacaRequest


def test_init():
    auth = AlpacaAuth(key="test_key", secret="test_secret")
    req = AlpacaRequest(auth=auth, rate_limit=1.0, timeout=30)
    # Validate the attributes are set correctly
    assert req._AlpacaRequest__auth.key == "test_key"
    assert req._AlpacaRequest__auth.secret == "test_secret"
    assert req._AlpacaRequest__limit == 1.0
    assert req._AlpacaRequest__timeout == 30


def test_get_request(mocker):
    mocker.patch("requests.get", return_value="some_response")
    req = AlpacaRequest()
    response = req.get("https://some.url")
    assert response == "some_response"


def test_post_request(mocker):
    mocker.patch("requests.post", return_value="post_response")
    req = AlpacaRequest()
    response = req.post("https://some.url", json={"key": "value"})
    assert response == "post_response"


def test_request_exception(mocker):
    mocker.patch("requests.get", side_effect=RequestException)
    req = AlpacaRequest()
    with pytest.raises(RequestException):
        req.get("https://some.url")


# Add more test cases for edge cases, rate limiting, and timeouts

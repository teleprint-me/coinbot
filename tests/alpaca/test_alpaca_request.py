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
    mocker.patch(
        "coinbot.api.alpaca.AlpacaRequest._request",
        return_value="get_response",
    )
    req = AlpacaRequest()
    response = req.get("https://some.url")
    assert response == "get_response"


def test_post_request(mocker):
    mocker.patch(
        "coinbot.api.alpaca.AlpacaRequest._request",
        return_value="post_response",
    )
    req = AlpacaRequest()
    response = req.post("https://some.url", json={"key": "value"})
    assert response == "post_response"


class MockResponse:
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.json_data


def test_page_request(mocker):
    mock_values = [
        MockResponse({"data": "page1", "next_page_token": "token1"}, 200),
        MockResponse({"data": "page2", "next_page_token": "token2"}, 200),
        MockResponse({"data": "page3", "next_page_token": None}, 200),
    ]

    def side_effect(*args, **kwargs):
        for value in mock_values:
            yield value

    mocker.patch(
        "coinbot.api.alpaca.AlpacaRequest.get",
        side_effect=side_effect(),
    )
    req = AlpacaRequest()

    # Collect responses from the generator
    responses = [
        res.json_data["data"]
        for res in req.page("https://some.url", params={"key": "value"})
    ]

    assert responses == ["page1", "page2", "page3"]


def test_request_exception(mocker):
    mocker.patch(
        "coinbot.api.alpaca.AlpacaRequest._request",
        side_effect=RequestException,
    )
    req = AlpacaRequest()
    with pytest.raises(RequestException):
        req.get("https://some.url")


# Add more test cases for edge cases, rate limiting, and timeouts

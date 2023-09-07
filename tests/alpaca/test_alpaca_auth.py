"""
tests/alpaca/test_alpaca_auth.py
"""
import logging

import pytest
from requests import PreparedRequest, Session

from coinbot.api.alpaca import AlpacaAuth, AlpacaRequest


@pytest.fixture(scope="module")
def alpaca_env() -> str:
    return ".env"


@pytest.fixture(scope="module")
def alpaca_auth(alpaca_env: str) -> AlpacaAuth:
    return AlpacaAuth(path=alpaca_env)


def test_init_with_env(alpaca_auth):
    assert alpaca_auth.key != ""
    assert alpaca_auth.secret != ""


def test_init_without_env():
    auth = AlpacaAuth(key="key_here", secret="secret_here")
    assert auth.key == "key_here"
    assert auth.secret == "secret_here"


def test_call_adds_headers(mocker, alpaca_auth):
    actual_request = PreparedRequest()
    actual_request.prepare(url="https://api.alpaca.markets/v2/positions", method="GET")
    updated_request = alpaca_auth(actual_request)
    assert "APCA-API-KEY-ID" in updated_request.headers
    assert "APCA-API-SECRET-KEY" in updated_request.headers


def test_logging(caplog):
    caplog.set_level(logging.DEBUG)

    # Manually instantiate to capture logs from constructor
    alpaca_auth = AlpacaAuth(key="your_key_here", secret="your_secret_here")

    # Validate that the log contains the desired text
    assert "Alpaca API Key:" in caplog.text

    # Prepare an actual request
    pr = PreparedRequest()
    pr.prepare(url="https://paper-api.alpaca.markets/v2/positions", method="GET")

    # Create a Session instance and send the request
    s = Session()
    s.send(alpaca_auth(pr))

    # Validate that the log contains the desired text
    assert "Censored Alpaca Header:" in caplog.text


def test_with_env_variables(monkeypatch):
    monkeypatch.setenv("PAPER_ALPACA_API_KEY", "mock_key")
    monkeypatch.setenv("PAPER_ALPACA_API_SECRET", "mock_secret")

    auth = AlpacaAuth()

    assert auth.key == "mock_key"
    assert auth.secret == "mock_secret"


def test_get_request(mocker):
    mocker.patch(
        "coinbot.api.alpaca.AlpacaRequest._request",
        return_value="get_response",
    )
    req = AlpacaRequest()
    response = req.get("https://some.url")
    assert response == "get_response"

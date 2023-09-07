"""
tests/alpaca/test_alpaca_endpoint.py
"""
import pytest

from coinbot.api.alpaca.endpoint import AlpacaEndpoint


@pytest.fixture(scope="module")
def alpaca_endpoint() -> AlpacaEndpoint:
    return AlpacaEndpoint()


def test_alpaca_subdomains(alpaca_endpoint):
    assert alpaca_endpoint.ALPACA_SUBDOMAINS == {
        "broker": {
            "paper": "https://broker-api.sandbox.alpaca.markets",
            "live": "https://broker-api.alpaca.markets",
        },
        "trade": {
            "paper": "https://paper-api.alpaca.markets",
            "live": "https://api.alpaca.markets",
        },
        "data": {
            "paper": "https://data.sandbox.alpaca.markets",
            "live": "https://data.alpaca.markets",
        },
    }


def test_normalize_url(alpaca_endpoint):
    assert alpaca_endpoint._normalize_url("endpoint") == "/endpoint"
    assert alpaca_endpoint._normalize_url("/endpoint") == "/endpoint"


def test_alpaca_build(alpaca_endpoint):
    assert (
        alpaca_endpoint.build("broker", "v2/positions", live=False)
        == "https://broker-api.sandbox.alpaca.markets/v2/positions"
    )
    assert (
        alpaca_endpoint.build("broker", "v2/positions", live=True)
        == "https://broker-api.alpaca.markets/v2/positions"
    )
    assert (
        alpaca_endpoint.build("broker", "/v2/positions", live=False)
        == "https://broker-api.sandbox.alpaca.markets/v2/positions"
    )
    assert (
        alpaca_endpoint.build("trade", "v2/positions", live=True)
        == "https://api.alpaca.markets/v2/positions"
    )

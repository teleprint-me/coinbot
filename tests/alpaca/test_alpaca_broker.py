"""
tests/alpaca/test_alpaca_broker.py
"""
import pytest

from coinbot.api.alpaca import AlpacaAuth, AlpacaBroker

# TODO: Implement Broker API support

# NOTE: These tests will fail until the Broker API key is provided
# NOTE: The AlpacaAuth needs to be passed the key and secret directly as arguments or it will default to the Trade API otherwise.
# def test_get_clock():
#     auth = AlpacaAuth(path=".env")
#     broker = AlpacaBroker(auth=auth)

#     result = broker.get_clock(live=False)

#     assert "is_open" in result
#     assert isinstance(result["is_open"], bool)
#     assert "timestamp" in result

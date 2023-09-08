"""
tests/alpaca/test_alpaca_trader.py
"""
import pytest

from coinbot.api.alpaca import AlpacaAuth, AlpacaTrader


def test_get_clock():
    auth = AlpacaAuth(path=".env")
    trader = AlpacaTrader(auth=auth)

    result = trader.get_clock(live=False)

    assert "is_open" in result
    assert isinstance(result["is_open"], bool)
    assert "timestamp" in result

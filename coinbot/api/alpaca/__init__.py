"""
Coinbot Alpaca API Integration

This module provides a convenient way to interact with the Alpaca API for trading and market data.
It includes the following components:

- AlpacaAuth: Authentication module for Alpaca API.
- AlpacaBroker: Broker module for managing brokerage-related operations.
- AlpacaMarketData: Market data module for retrieving real-time and historical market data.
- AlpacaTrader: Trading module for executing orders and managing positions.

Example Usage:
--------------
from coinbot.api.alpaca import AlpacaAuth, AlpacaBroker, AlpacaMarketData, AlpacaTrader

# Initialize authentication
auth = AlpacaAuth(".env")

# Initialize broker
broker = AlpacaBroker(auth)

# Initialize market data module
marketer = AlpacaMarketData(auth)

# Initialize trader module
trader = AlpacaTrader(auth)

# Use the components for trading and market data operations.
"""

from coinbot.api.alpaca.auth import AlpacaAuth
from coinbot.api.alpaca.broker import AlpacaBroker
from coinbot.api.alpaca.data import AlpacaMarketData
from coinbot.api.alpaca.trade import AlpacaTrader

__all__ = ["AlpacaAuth", "AlpacaBroker", "AlpacaMarketData", "AlpacaTrader"]

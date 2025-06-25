"""
coinbot/trade.py
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import click

from coinbot import logging
from coinbot.api.alpaca import AlpacaAuth, AlpacaMarketData, AlpacaTrader
from coinbot.db import ValueAveragingDatabase


@click.command()
@click.argument(  # Argument is required
    "symbol",  # Can be Stock or Crypto Symbol
    type=click.STRING,
    default="ETH/BTC",
)
@click.argument(  # Argument is required
    # Number of shares to trade.
    # Can be fractionable for only market and day order types.
    "quantity",
    type=click.FLOAT,
    default=0.0005,
)
@click.option(  # this option is required
    "--side",
    type=click.Choice(["buy", "sell"]),
    default="buy",
    help="Represents which side this order was on. Default is buy.",
)
@click.option(  # this option is required
    "--type_",
    type=click.Choice(["market", "limit", "stop", "stop_limit", "trailing_stop"]),
    default="market",
    help="Represents the types of orders Alpaca currently supports.",
)
@click.option(  # this option is required
    "--time_in_force",
    type=click.Choice(["day", "gtc", "opg", "cls", "ioc", "fok"]),
    default="ioc",
    help="Time in Force. Crypto Trading supports day, gtc, ioc and fok. OPG and CLS are not supported.",
)
@click.option(
    "--rate",
    type=click.FLOAT,
    default=0.10,
    help="The annual interest rate. Default is 0.10.",
)
@click.option(
    "--frequency",
    type=click.INT,
    default=365,
    help="How often interest is compounded per year. Default is 365.",
)
@click.option(
    "--interval",
    type=click.INT,
    default=1,
    help="The time step between each trade. Default is 1.",
)
@click.option(
    "--live",
    type=click.BOOL,
    default=False,
    help="The API URL for paper or live trading. Default is paper.",
)
@click.option(
    "--database",
    type=click.STRING,
    default="value_averaging.sqlite",
    help="The database file path. Default is value_averaging.sqlite.",
)
def main():
    def calculate_target_value(config):
        P = config["initial_principal"]
        r = config["annual_interest_rate"]
        n = config["compounding_frequency"]
        i = config["current_interval"]

        T = P * i * (1 + (r / n)) ** i
        return T

    with open("config.json", "r") as f:
        config = json.load(f)

    auth = AlpacaAuth(path=".env")
    trader = AlpacaTrader(auth=auth)
    marketer = AlpacaMarketData(auth=auth)

    result = trader.get_current_asset_value("BTC/USD")
    pprint(result)

    # NOTE: Table Collisions
    # Collisions can occur if the assets table exists as a simulation.
    # NOTE: State Management
    # Given you're working with real-time data, you'll need to update current_interval, market_price, and current_value at each trading action. If you're using a database with Peewee, these could be fields in your database model, or you could update them directly in your JSON config for a quick-and-dirty approach.
    # asset_name = symbols.split("/")[0]
    # va = ValueAveraging(
    #     asset_name=asset_name,
    #     principal_amount=principal,
    #     interest_rate=rate,
    #     frequency=frequency,  # Using daily candlesticks
    #     interval=interval,  # Starting interval
    # )
    # Connect to database and get model
    db = ValueAveragingDatabase(database)
    db.connect()
    asset_model = db.get_model(symbol)

    # Query data and convert to DataFrame
    data = list(asset_model.select().dicts())
    df = pd.DataFrame(data)
    ...


if __name__ == "__main__":
    main()

"""
coinbot/trade.py
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import click

from coinbot import logging
from coinbot.api import alpaca
from coinbot.model.database import ValueAveragingDatabase


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
    "--url",
    type=click.STRING,
    default="https://paper-api.alpaca.markets/v2/orders",
    help="The API URL for paper or live trading. Default is paper.",
)
@click.option(
    "--database",
    type=click.STRING,
    default="value_averaging.sqlite",
    help="The database file path. Default is value_averaging.sqlite.",
)
def main():
    # NOTE: We can use alpaca.get and alpaca.post for making authenticated requests
    # They're just special wrappers handling the defaults for us
    # def get(url: str, params: Optional[Dict] = None) -> Response:
    #     """Perform a GET request to the specified API path.
    #
    #     Args:
    #         path: The API endpoint to be requested.
    #         params: (optional) Query parameters to be passed with the request.
    #
    #     Returns:
    #         The response of the GET request.
    #     """
    # def post(url: str, json: Optional[Dict] = None) -> Response:
    #     """Perform a POST request to the specified API path.

    #     Args:
    #         path: The API endpoint to be requested.
    #         json: (optional) JSON payload to be sent with the request.

    #     Returns: The response of the POST request.
    #     """
    # NOTE: Conflicts can occur if the assets table exists as a simulation.
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

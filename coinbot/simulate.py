"""
coinbot/sample.py
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import click

from coinbot import logging
from coinbot.strategy.value_average import ValueAveraging


@click.command()
@click.option(
    "--symbols", default="BTC/USD", help="Crypto symbols to sample. Default is BTC/USD."
)
@click.option(
    "--timeframe",
    default="1D",
    help="Timeframe for sampling. Default is 1D. Possible values: '1D', '1H', '15T', etc.",
)
@click.option(
    "--start",
    default=None,
    help="Start date-time for sampling. Format: RFC-3339 or YYYY-MM-DD.",
)
@click.option(
    "--end",
    default=None,
    help="End date-time for sampling. Format: RFC-3339 or YYYY-MM-DD.",
)
@click.option(
    "--loc",
    default="us",
    help="The location for sampling. Default is us. Possible values: 'us', etc.",
)
@click.option(
    "--principal",
    default=100.00,
    help="The principal amount. Default is 100. Specify as a decimal value.",
)
@click.option(
    "--rate",
    default=0.10,
    help="The annual interest rate. Default is 0.10. Specify as a decimal value.",
)
@click.option(
    "--frequency",
    default=365,
    help="How often interest is compounded per year. Default is 365. Specify as an integer value.",
)
@click.option(
    "--interval",
    default=1,
    help="The time step between each trade. Default is 1. Specify as an integer value.",
)
def main(symbols, timeframe, start, end, loc, principal, rate, frequency, interval):
    if "," in symbols or "/" not in symbols:
        logging.error(
            "Please provide a single asset class in the format 'ASSET/CURRENCY'"
        )
        return

    if start is None:
        dt_start = datetime.now(timezone.utc) - timedelta(days=1)
    else:
        dt_start = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)

    if end is None:
        dt_end = datetime.now(timezone.utc)
    else:
        dt_end = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)

    params = {
        "symbols": symbols,
        "timeframe": timeframe,
        "start": dt_start.isoformat(),
        "end": dt_end.isoformat(),
    }

    sampled = alpaca.page_crypto_candlesticks(loc, params)

    if not sampled:
        logging.warning(f"No results for {symbols} from {start} to {end}")
        return

    asset_name = symbols.split("/")[0]
    va = ValueAveraging(
        asset_name=asset_name,
        principal_amount=principal,
        interest_rate=rate,
        frequency=frequency,  # Using daily candlesticks
        interval=interval,  # Starting interval
    )
    logging.info(
        f"Initialized ValueAveraging with {va.principal_amount} principal at {va.interest_rate} APY."
    )

    # key: str = "BTC/USD"
    # results: List[Dict[str, str | int | float]] = [
    #     {
    #       "t": "2022-05-27T10:18:00Z",
    #       "o": 28999,
    #       "h": 29003,
    #       "l": 28999,
    #       "c": 29003,
    #       "v": 0.01,
    #       "n": 4,
    #       "vw": 29001
    #     }
    # ]
    #
    # Flag to check if the first record is initialized
    is_first_record_initialized = False

    for key, results in sampled.items():
        # Initialize if first record
        if not is_first_record_initialized:
            first_market_price = results[0]["c"]
            va.initialize_first_record(
                market_price=first_market_price, datetime=results[0]["t"]
            )
            is_first_record_initialized = True
            start_index = 1  # Skip the first record in the subsequent loop
        else:
            start_index = 0  # Include all records

        # Process the sampled data
        for i in range(start_index, len(results)):
            result = results[i]
            if "c" in result and "t" in result:
                market_price = result["c"]
                dt = result["t"]
                va.update_records(market_price, dt)
            else:
                logging.warning("Skipping record due to missing 'c' or 't' fields.")

    va.db.close()


if __name__ == "__main__":
    main()

# Historical bars
#
# GET https://data.alpaca.markets/v1beta3/crypto/{loc}/bars
# The crypto bars API provides historical aggregates for a list of crypto symbols between the specified dates.
#
# PATH PARAMS
# loc string required
# Crypto location, e.g. us
#
# QUERY PARAMS
# symbols string required
# Comma separated list of symbols, e.g. "BTC/USD,LTC/USD"
#
# timeframe string required
# The timeframe of the bar aggregation. 5Min for example creates 5 minute aggregates, e.g. 1Min
# You can use the following values:
#
# - [1-59]Min / T
# - [1-23]Hour / H
# - 1Day / D
# - 1Week / W
# - [1,2,3,4,6,12]Month / M
#
# start date-time
# The inclusive start of the interval. Format: RFC-3339 or YYYY-MM-DD.
# If missing, the default value is the beginning of the current day.
#
# end date-time
# The inclusive end of the interval. Format: RFC-3339 or YYYY-MM-DD.
# If missing, the default value is the current time.
#
# date-time usage example: 2022-01-04T01:02:03.123456789Z
#
# limit int64
# Number of maximum data points to return in a response.
# The limit applies to the total number of data points, not per symbol!
# You can use the next_page_token to fetch the next at most limit responses.
#
# page_token string
# Pagination token to continue from. The value to pass here is returned in specific requests when more data is available than the request limit allows.
#
# sort string
# Sort data in ascending or descending order.
#
# Response
# 200 ok
#
# {
#   "bars": {
#     "BTC/USD": [
#       {
#         "t": "2022-05-27T10:18:00Z",
#         "o": 28999,
#         "h": 29003,
#         "l": 28999,
#         "c": 29003,
#         "v": 0.01,
#         "n": 4,
#         "vw": 29001
#       }
#     ]
#   },
#   "next_page_token": null
# }

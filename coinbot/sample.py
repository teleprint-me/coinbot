"""
coinbot/sample.py
"""
from datetime import datetime, timedelta, timezone
from typing import Any, List

import click

from coinbot import logging
from coinbot.api import alpaca


@click.command()
@click.option("--symbols", default="BTC/USD", help="Crypto symbols to sample.")
@click.option("--timeframe", default="1D", help="Timeframe for sampling.")
@click.option("--start", default=None, help="Start date-time.")
@click.option("--end", default=None, help="End date-time.")
def main(symbols, timeframe, start, end):
    start = datetime(2023, 1, 1, tzinfo=timezone.utc)
    end = datetime(2023, 1, 30, tzinfo=timezone.utc)
    params = {
        "symbols": symbols,
        "timeframe": timeframe,
        "start": start.isoformat("T"),
        "end": end.isoformat("T"),
    }

    sampled = alpaca.get_crypto_candlesticks("us", params)
    dataset = sampled.get("BTC/USD")

    assert bool(dataset) is True, f"Expected results for BTC/USD from {start} to {end}"

    for dataframe in dataset:
        logging.info(dataframe)


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

"""
coinbot/sample.py
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import click

from coinbot import logging
from coinbot.api import alpaca


@click.command()
@click.option("--symbols", default="BTC/USD", help="Crypto symbols to sample.")
@click.option("--timeframe", default="1D", help="Timeframe for sampling.")
@click.option(
    "--start", default=None, help="Start date-time. Format: RFC-3339 or YYYY-MM-DD"
)
@click.option(
    "--end", default=None, help="End date-time. Format: RFC-3339 or YYYY-MM-DD"
)
@click.option("--loc", default="us", help="The location for sampling.")
def main(symbols, timeframe, start, end, loc):
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

    for key, results in sampled.items():
        # TODO: process the sampled data
        print(key)
        for result in results:
            print(result)


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

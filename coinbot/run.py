"""
coinbot/run.py
"""
from pprint import pprint

from coinbot.model.value_average import ValueAveraging

# Example usage:
va = ValueAveraging(principal_amount=10, interest_rate=0.10, frequency=12)
va.initialize_first_record(market_price=9334.98, datetime="2020-01-01")
va.update_records(8_505.07, datetime="2020-02-01")
pprint(va.records)

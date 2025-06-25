"""
coinbot/model/value_average.py
"""
from decimal import ROUND_HALF_EVEN, Decimal
from sqlite3 import IntegrityError, OperationalError
from typing import Dict, List, Optional

from iso8601 import parse_date

from coinbot import logging
from coinbot.db import ValueAveragingDatabase


class ValueAveraging:
    def __init__(
        self,
        asset_name: str,
        principal_amount: float,
        interest_rate: float,
        frequency: Optional[int] = 365,  # defaults to daily
        interval: Optional[int] = 1,
        base_precision: Optional[int] = 8,
        quote_precision: Optional[int] = 2,
    ):
        self.asset_name = asset_name  # set the asset name
        self.db = ValueAveragingDatabase()  # create peewee database
        self.model = self.db.get_model(asset_name)  # create model and open db
        self.interval = 1
        self.prev_total_order_size = self.round_decimal("0", base_precision)
        self.prev_total_trade_amount = self.round_decimal("0", base_precision)
        self.principal_amount = self.round_decimal(principal_amount, quote_precision)
        self.interest_rate = self.round_decimal(interest_rate, quote_precision)
        self.frequency = frequency

    def round_decimal(self, value, decimal_places) -> Decimal:
        return Decimal(value).quantize(
            Decimal(f"1e-{decimal_places}"), rounding=ROUND_HALF_EVEN
        )

    def calculate_trade_amount(self, target_amount: float, current_value: float):
        # Calculate the trade amount as the difference between the target amount and the current value
        current_trade_amount = target_amount - current_value
        return current_trade_amount

    def get_target_amount(self, interval: int):
        rate_per_compounding_period = self.interest_rate / self.frequency

        # Calculate the Current Target amount using the adapted Value Averaging formula
        current_target_amount = (
            self.principal_amount
            * interval
            * (1 + rate_per_compounding_period) ** interval
        )
        return current_target_amount

    def initialize_first_record(
        self, market_price: float, datetime: str, precision: Optional[int] = 2
    ):
        datetime = parse_date(datetime)
        market_price = self.round_decimal(market_price, precision)
        current_target = self.principal_amount  # Initial principal amount
        order_size = self.principal_amount / market_price
        total_order_size = order_size + self.prev_total_order_size
        current_value = market_price * self.prev_total_order_size
        trade_amount = self.principal_amount - current_value
        total_trade_amount = trade_amount + self.prev_total_trade_amount

        # Rounding for precision
        current_value = self.round_decimal(current_value, precision)
        order_size = self.round_decimal(
            order_size, 8
        )  # Rounded to 8 decimal places for satoshis
        total_order_size = self.round_decimal(total_order_size, 8)
        trade_amount = self.round_decimal(
            trade_amount, 2
        )  # Rounded to 2 decimal places for cents
        total_trade_amount = self.round_decimal(total_trade_amount, 2)

        # Persist to database
        record = self.model(
            exchange="paper",
            date=datetime,
            market_price=market_price,
            current_target=current_target,
            current_value=current_value,
            trade_amount=trade_amount,
            total_trade_amount=total_trade_amount,
            order_size=order_size,
            total_order_size=total_order_size,
            interval=self.interval,
        )

        try:
            record.save()
            logging.info("Successfully saved the record to the database.")
        except OperationalError as oe:
            logging.error(f"Failed to save the record: {oe}")
        except IntegrityError as ie:
            logging.error(f"Integrity Error: {ie}")

        # Update the class variables for next calculations
        self.prev_total_order_size = total_order_size
        self.prev_total_trade_amount = total_trade_amount
        self.interval += 1

    def update_records(self, market_price, datetime, precision: Optional[int] = 2):
        datetime = parse_date(datetime)
        market_price = self.round_decimal(market_price, precision)
        current_target = self.get_target_amount(self.interval)
        current_value = market_price * self.prev_total_order_size
        trade_amount = self.calculate_trade_amount(current_target, current_value)
        total_trade_amount = trade_amount + self.prev_total_trade_amount
        order_size = trade_amount / market_price
        total_order_size = order_size + self.prev_total_order_size

        # Rounding for precision
        current_target = self.round_decimal(current_target, precision)
        current_value = self.round_decimal(current_value, precision)
        order_size = self.round_decimal(order_size, 8)
        total_order_size = self.round_decimal(total_order_size, 8)
        trade_amount = self.round_decimal(trade_amount, 2)
        total_trade_amount = self.round_decimal(total_trade_amount, 2)

        # Persist to database
        record = self.model(
            exchange="paper",
            date=datetime,
            market_price=market_price,
            current_target=current_target,
            current_value=current_value,
            trade_amount=trade_amount,
            total_trade_amount=total_trade_amount,
            order_size=order_size,
            total_order_size=total_order_size,
            interval=self.interval,
        )

        try:
            record.save()
            logging.info("Successfully saved the record to the database.")
        except OperationalError as oe:
            logging.error(f"Failed to save the record: {oe}")
        except IntegrityError as ie:
            logging.error(f"Integrity Error: {ie}")

        # Update the class variables for next calculations
        self.prev_total_order_size = total_order_size
        self.prev_total_trade_amount = total_trade_amount
        self.interval += 1

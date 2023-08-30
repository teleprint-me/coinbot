from decimal import ROUND_HALF_EVEN, Decimal
from typing import Dict, List, Optional


class ValueAveraging:
    def __init__(
        self,
        principal_amount: float,
        interest_rate: float,
        frequency: int,
        base_precision: Optional[int] = 8,
        quote_precision: Optional[int] = 2,
    ):
        self.interval = 1
        self.prev_total_order_size = self.round_decimal("0", base_precision)
        self.prev_total_trade_amount = self.round_decimal("0", base_precision)
        self.principal_amount = self.round_decimal(principal_amount, quote_precision)
        self.interest_rate = self.round_decimal(interest_rate, quote_precision)
        self.frequency = frequency
        self.records: List[Dict[str, str | float | int]] = []

    def round_decimal(self, value, decimal_places) -> Decimal:
        return Decimal(value).quantize(
            Decimal(f"1e-{decimal_places}"), rounding=ROUND_HALF_EVEN
        )

    def calculate_trade_amount(self, target_amount, current_value):
        # Calculate the trade amount as the difference between the target amount and the current value
        current_trade_amount = target_amount - current_value
        return current_trade_amount

    def get_target_amount(self, interval):
        rate_per_compounding_period = self.interest_rate / self.frequency

        # Calculate the Current Target amount using the adapted Value Averaging formula
        current_target_amount = (
            self.principal_amount
            * interval
            * (1 + rate_per_compounding_period) ** interval
        )
        return current_target_amount

    def initialize_first_record(
        self, market_price, datetime, precision: Optional[int] = 2
    ):
        market_price = self.round_decimal(market_price, precision)
        current_target = self.principal_amount  # Initial principal amount
        order_size = self.principal_amount / market_price
        total_order_size = order_size + self.prev_total_order_size
        current_value = market_price * self.prev_total_order_size
        trade_amount = self.principal_amount - current_value
        total_trade_amount = trade_amount + self.prev_total_trade_amount

        # Rounding for precision
        order_size = self.round_decimal(
            order_size, 8
        )  # Rounded to 8 decimal places for satoshis
        total_order_size = self.round_decimal(total_order_size, 8)
        trade_amount = self.round_decimal(
            trade_amount, 2
        )  # Rounded to 2 decimal places for cents
        total_trade_amount = self.round_decimal(total_trade_amount, 2)

        # Create a dictionary to store these values
        record = {
            "Exchange": "paper",
            "Date": datetime,
            "Market Price": market_price,
            "Current Target": current_target,
            "Current Value": current_value,
            "Trade Amount": trade_amount,
            "Total Trade Amount": total_trade_amount,
            "Order Size": order_size,
            "Total Order Size": total_order_size,
            "Interval": self.interval,
        }

        # Instantiate the initial record as a list of records
        self.records = [record]

        # Update the class variables for next calculations
        self.prev_total_order_size = total_order_size
        self.prev_total_trade_amount = total_trade_amount
        self.interval += 1


# Example usage:
va = ValueAveraging(principal_amount=10, interest_rate=0.05, frequency=12)
va.initialize_first_record(market_price=9334.98, datetime="2020-01-01")
print(va.records)

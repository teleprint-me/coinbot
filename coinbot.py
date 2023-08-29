class ValueAveraging:
    def __init__(self):
        self.interval = 1
        self.prev_total_order_size = 0
        self.prev_total_trade_amount = 0
        self.principal_amount = 10
        self.interest_rate = 0.10
        self.frequency = 12
        self.growth_rate = 1 + (self.interest_rate / self.frequency)
        self.records = []

    @staticmethod
    def calculate_trade_amount(
        principal, annual_rate, compounding_frequency, time_period
    ):
        # Calculate the target amount using the compound interest formula
        target_amount = principal * (1 + annual_rate / compounding_frequency) ** (
            compounding_frequency * time_period
        )

        # Calculate the trade amount as the difference between the target amount and the current principal
        trade_amount = target_amount - principal

        return target_amount, trade_amount

    def initialize_first_record(self, market_price, datetime):
        current_target = self.principal_amount  # Initial principal amount
        order_size = self.principal_amount / market_price
        total_order_size = order_size + self.prev_total_order_size
        current_value = market_price * self.prev_total_order_size
        trade_amount = self.principal_amount - current_value
        total_trade_amount = trade_amount + self.prev_total_trade_amount

        # Rounding for precision
        order_size = round(order_size, 8)  # Rounded to 8 decimal places for satoshis
        total_order_size = round(total_order_size, 8)
        trade_amount = round(trade_amount, 2)  # Rounded to 2 decimal places for cents
        total_trade_amount = round(total_trade_amount, 2)

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

        # Append this record to our list of records
        self.records.append(record)

        # Update the class variables for next calculations
        self.prev_total_order_size = total_order_size
        self.prev_total_trade_amount = total_trade_amount
        self.interval += 1


# Example usage:
va = ValueAveraging()
va.initialize_first_record(9334.98, "2020-01-01")
print(va.records)

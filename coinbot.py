def calculate_trade_amount(principal, annual_rate, compounding_frequency, time_period):
    # Calculate the target amount using the compound interest formula
    target_amount = principal * (1 + annual_rate / compounding_frequency) ** (
        compounding_frequency * time_period
    )

    # Calculate the trade amount as the difference between the target amount and the current principal
    trade_amount = target_amount - principal

    return target_amount, trade_amount


# Example usage:
principal = 1000  # Initial investment in USD
annual_rate = 0.1  # 10% annual gain as a decimal
compounding_frequency = 365  # Compounded daily
time_period = 1  # Time in years

target_amount, trade_amount = calculate_trade_amount(
    principal, annual_rate, compounding_frequency, time_period
)

print(f"Target Amount: {target_amount}")
print(f"Trade Amount: {trade_amount}")

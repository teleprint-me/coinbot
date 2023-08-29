import numpy as np
import pandas as pd

# Given sample dataset
data = {
    "Exchange": ["paper"] * 12,
    "Date": [
        "01/01/20",
        "02/01/20",
        "03/01/20",
        "04/01/20",
        "05/01/20",
        "06/01/20",
        "07/01/20",
        "08/01/20",
        "09/01/20",
        "10/01/20",
        "11/01/20",
        "12/01/20",
    ],
    "Market Price": [
        9334.98,
        8505.07,
        6424.35,
        8624.28,
        9446.57,
        9136.20,
        11351.62,
        11655.00,
        10779.63,
        13804.81,
        19713.94,
        28990.08,
    ],
}

df = pd.DataFrame(data)


# Function to round numbers to the nearest base
def round_to_base(x, base=0.01):
    return round(base * round(float(x) / base), 8)


# Initialize variables with updated values
principal_amount = 10.00  # constant float value in USD
annual_interest_rate = 0.10  # 10% annual gain as a decimal
frequency = 12  # monthly
time_period = 1 + (annual_interest_rate / frequency)  # Calculate Growth Rate

# Initialize tracking variables again for the simplified formula
previous_total_order_size = 0.0
previous_total_trade_amount = 0.0
interval = 1

# Initialize the DataFrame again for the new calculations
df["Current Target"] = np.nan
df["Current Value"] = np.nan
df["Trade Amount"] = np.nan
df["Total Trade Amount"] = np.nan
df["Order Size"] = np.nan
df["Total Order Size"] = np.nan
df["Interval"] = np.nan

# Loop through each record to recalculate values with the simplified formula
for index, row in df.iterrows():
    # Get Interval
    df.at[index, "Interval"] = interval

    # Get Current Target using the simplified formula
    if interval == 1:
        current_target = principal_amount
    else:
        current_target = (principal_amount * interval) * (
            1 + annual_interest_rate / frequency
        ) ** (frequency * time_period)

    current_target = round_to_base(current_target, 0.01)  # rounding to the nearest cent
    df.at[index, "Current Target"] = current_target

    # Other calculations remain the same as in the previous code
    current_value = round_to_base(
        row["Market Price"] * previous_total_order_size, 0.01
    )  # rounding to the nearest cent
    df.at[index, "Current Value"] = current_value
    trade_amount = round_to_base(
        current_target - current_value, 0.01
    )  # rounding to the nearest cent
    df.at[index, "Trade Amount"] = trade_amount
    order_size = round_to_base(
        trade_amount / row["Market Price"], 0.00000001
    )  # rounding to the nearest satoshi
    df.at[index, "Order Size"] = order_size
    total_order_size = round_to_base(
        previous_total_order_size + order_size, 0.00000001
    )  # rounding to the nearest satoshi
    df.at[index, "Total Order Size"] = total_order_size
    total_trade_amount = round_to_base(
        previous_total_trade_amount + trade_amount, 0.01
    )  # rounding to the nearest cent
    df.at[index, "Total Trade Amount"] = total_trade_amount

    # Update tracking variables for next iteration
    previous_total_order_size = total_order_size
    previous_total_trade_amount = total_trade_amount
    interval += 1

print(df)

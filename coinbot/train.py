"""
coinbot/train.py
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from coinbot.model.base import Layer  # assuming your base Layer is here
from coinbot.model.dense import Dense  # assuming your Dense layer is here

# Your data
data = [
    [
        "paper",
        "01/01/20",
        9334.98,
        10.00,
        0.00,
        10.00,
        10.00,
        0.00107124,
        0.00107124,
        1,
    ],
    # ... more rows
]

# Convert data to a pandas DataFrame for easier manipulation
df = pd.DataFrame(
    data,
    columns=[
        "Exchange",
        "Date",
        "Market Price",
        "Current Target",
        "Current Value",
        "Trade Amount",
        "Total Trade Amount",
        "Order Size",
        "Total Order Size",
        "Interval",
    ],
)

# Label encoding for 'Exchange'
label_encoder = LabelEncoder()
df["Exchange"] = label_encoder.fit_transform(df["Exchange"])

# One-hot encoding for 'Exchange'
onehot_encoder = OneHotEncoder()
exchange_onehot = onehot_encoder.fit_transform(df[["Exchange"]]).toarray()
exchange_onehot_df = pd.DataFrame(
    exchange_onehot,
    columns=[f"Exchange_{int(i)}" for i in range(exchange_onehot.shape[1])],
)
df = pd.concat([df, exchange_onehot_df], axis=1).drop(["Exchange"], axis=1)

# Break down 'Date' into year, month, and day
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df.drop(["Date"], axis=1, inplace=True)

# Your input and output
X = df.drop(
    ["Current Target"], axis=1
).to_numpy()  # assuming 'Current Target' is what you're trying to predict
y = df["Current Target"].to_numpy()

# Initialize your layers and neural network here, for example:
input_dim = X.shape[1]
output_dim = 1  # or whatever it is for 'Current Target'
dense_layer = Dense(input_dim, output_dim)

# Forward pass
output = dense_layer.forward(X)

# Backward pass and parameter update
# ...

# Decode the output back to original labels if needed
# ... (use inverse_transform() from label_encoder or onehot_encoder)

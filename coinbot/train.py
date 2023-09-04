"""
coinbot/train.py
"""
import click
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from coinbot import logging
from coinbot.model.database import ValueAveragingDatabase
from coinbot.model.dense import Trainer


@click.command()
@click.argument(
    "input_id",
    type=click.STRING,
    default="BTC",
)
@click.argument(
    "output_id",
    type=click.Path(exists=True),
    default="models/coinbot.dnn.npy",
)
@click.option(
    "--database",
    default=None,
    help="The name of the database. Default is None.",
)
@click.option(
    "--layers",
    default=3,
    help="The number of layers the model should have. Default is None.",
)
@click.option(
    "--parameters",
    default=5,
    help="The number of parameters the model should have. Default is None.",
)
def main(input_id, output_id, database, layers, parameters):
    # Load Simulated Data for Preprocessing

    # Connect to database and get model
    db = ValueAveragingDatabase(database)
    db.connect()
    asset_model = db.get_model(input_id)

    # Query data and convert to DataFrame
    data = list(asset_model.select().dicts())
    df = pd.DataFrame(data)

    # Data Preprocessing

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
    ).to_numpy()  # assuming 'Trade Amount' is what you're trying to predict
    y = df["Trade Amount"].to_numpy()

    # Train the network
    trainer = Trainer(X, y, architecture, epochs=5000, learning_rate=0.1)
    trainer.run_training()
    trainer.save_model(output_id)

    # Log completion
    logging.info(f"Model trained and saved at {output_id}")


if __name__ == "__main__":
    main()

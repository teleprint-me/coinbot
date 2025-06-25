"""
coinbot/xor.py

"Hello, World!"
"""
import os

import click
import numpy as np

from coinbot import logging
from coinbot.model.dense import Trainer


@click.command()
@click.option(
    "--model_id",
    type=click.STRING,
    default="models/coinbot-xor.h5",
    help="The file path for the model. Default is 'models/coinbot-xor.h5'.",
)
@click.option(
    "--epochs",
    type=click.INT,
    default=10_000,
    help="Number of training epochs. Default is 10,000.",
)
@click.option(
    "--learning_rate",
    type=click.FLOAT,
    default=0.15,
    help="Learning rate for the training process. Default is 0.15.",
)
@click.option(
    "--lambda_",
    type=click.FLOAT,
    default=1e-5,
    help="L2 regularization parameter. Default is 1e-5.",
)
@click.option(
    "--tolerance",
    type=click.FLOAT,
    default=1e-5,
    help="Tolerance for early stopping during training. Default is 1e-5.",
)
def main(model_id, epochs, learning_rate, lambda_, tolerance):
    # Input for XOR logic
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

    # Output for XOR logic
    y = np.array([[0], [1], [1], [0]])

    # Network architecture
    architecture = [
        {"type": "Dense", "input_dim": 2, "output_dim": 2},
        {"type": "Tanh"},
        {"type": "Dense", "input_dim": 2, "output_dim": 1},
        {"type": "Tanh"},
    ]

    # Initialize trainer
    trainer = Trainer(
        X,
        y,
        architecture,
        epochs=10000,
        learning_rate=learning_rate,
        lambda_=lambda_,
        tolerance=tolerance,
    )

    if model_id and os.path.exists(model_id):
        trainer.load_model(model_id)
        logging.info(f"Loaded model: {model_id}")
    else:  # Perform training
        trainer.run_training()

    # Test the trained model
    print("Running predictions:")
    output = trainer.run_prediction(X)
    print(output)

    metadata = trainer.get_metadata()
    print(metadata)

    # Save the model and check if it can be loaded
    if model_id and not os.path.exists(model_id):
        trainer.save_model(model_id)
        logging.info(f"Saved model: {model_id}")
    else:
        logging.info(f"Preserved model: {model_id}")


if __name__ == "__main__":
    main()

"""
coinbot/xor.py

"Hello, World!"
"""
import os

import numpy as np

from coinbot import logging
from coinbot.model.dense import Trainer

filename = "coinbot-xor.h5"

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
trainer = Trainer(X, y, architecture, epochs=10000)

if os.path.exists(filename):
    trainer.load_model(filename)
    logging.info(f"{filename} exists. Loaded model and skipping training.")
else:
    # Perform training
    trainer.run_training()

# Test the trained model
print("Running predictions:")
output = trainer.run_prediction(X)
print(output)

metadata = trainer.get_metadata()
print(metadata)

# Save the model and check if it can be loaded
if not os.path.exists(filename):
    trainer.save_model(filename)
else:
    logging.info(f"{filename} exists. Prevented overwriting model.")

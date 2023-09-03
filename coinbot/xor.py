"""
coinbot/xor.py

"Hello, World!"
"""
import numpy as np

from coinbot.model.dense import Dense
from coinbot.model.error import mse, mse_prime
from coinbot.model.tanh import Tanh

X = []
Y = []

network = [Dense(2, 3), Tanh(), Dense(3, 1), Tanh]

epochs = 10_000
learning_rate = 0.1

for epoch in range(epochs):
    ...

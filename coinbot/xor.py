"""
coinbot/xor.py

"Hello, World!"
"""
import numpy as np

from coinbot.model.dense import Dense, Tanh, mse, mse_prime

# Input for XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# Output for XOR
Y = np.array([[0], [1], [1], [0]])

# Network architecture
network = [Dense(2, 3), Tanh(), Dense(3, 1), Tanh()]

# Training parameters
epochs = 10000
learning_rate = 0.1

# Training loop
for epoch in range(epochs):
    # Forward pass
    output = X
    for layer in network:
        output = layer.forward(output)

    # Calculate loss
    loss = mse(Y, output)

    # Backward pass
    gradient = mse_prime(Y, output)
    for layer in reversed(network):
        gradient = layer.backward(gradient, learning_rate)

    # Print loss every 1000 epochs
    if epoch % 1000 == 0:
        print(f"Epoch {epoch}, Loss: {loss}")

# Test the network
output = X
for layer in network:
    output = layer.forward(output)

print("Predictions after training:")
print(output)

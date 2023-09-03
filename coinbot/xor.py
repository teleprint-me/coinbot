"""
coinbot/xor.py

"Hello, World!"
"""
import numpy as np

from coinbot.model.dense import Dense, Tanh, mse_prime, regularized_mse

# Input for XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# Output for XOR
Y = np.array([[0], [1], [1], [0]])

# Network architecture
network = [Dense(2, 3), Tanh(), Dense(3, 1), Tanh()]

# Training parameters
epochs = 10000
learning_rate = 0.15
lambda_ = 1e-5  # L2 regularization
tolerance = 1e-5  # Tolerance for early stopping
prev_loss = None  # To store the previous loss

# Training loop
for epoch in range(epochs):
    # Forward pass
    output = X
    for layer in network:
        output = layer.forward(output)

    # Extract weights for regularization from the Dense layers
    # and concatenate all the weights into one flat array
    weights = [layer.weights for layer in network if isinstance(layer, Dense)]
    all_weights = np.concatenate([w.flatten() for w in weights])
    # Calculate loss with regularization
    loss = regularized_mse(Y, output, all_weights, lambda_)

    # Check for early stopping
    if prev_loss is not None:
        if abs(prev_loss - loss) < tolerance:
            print(f"Early stopping on epoch {epoch}, Loss: {loss}")
            break

    # Backward pass
    gradient = mse_prime(Y, output)
    for layer in reversed(network):
        gradient = layer.backward(gradient, learning_rate, lambda_)

    # Print loss every 1000 epochs
    if epoch % 1000 == 0:
        print(f"Epoch {epoch}, Loss: {loss}")

    prev_loss = loss  # Update the previous loss

# Test the network
output = X
for layer in network:
    output = layer.forward(output)

print("Predictions after training:")
print(output)

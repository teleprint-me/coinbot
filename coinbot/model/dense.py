"""
coinbot/model/dense.py
"""
from abc import abstractmethod

import numpy as np

from coinbot import logging


def mse(y_true, y_pred):
    return np.mean(np.square(y_true - y_pred))


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def regularized_mse(y_true, y_pred, weights, lambda_):
    mse_loss = np.mean(np.square(y_true - y_pred))
    l2_penalty = lambda_ * np.sum(np.square(weights))
    return mse_loss + l2_penalty


class Layer:
    def __init__(self):
        ...

    @abstractmethod
    def forward(self, input_data):
        ...

    @abstractmethod
    def backward(self, output_gradient, learning_rate, lambda_):
        ...


class Dense(Layer):
    def __init__(self, input_dim, output_dim):
        self.weights = np.random.randn(input_dim, output_dim)
        self.biases = np.zeros((1, output_dim))

    def forward(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.biases
        return self.output

    def backward(self, output_gradient, learning_rate, lambda_):
        input_gradient = np.dot(output_gradient, self.weights.T)
        weights_gradient = np.dot(self.input.T, output_gradient)

        # Update parameters with regularization
        self.weights -= learning_rate * (weights_gradient + 2 * lambda_ * self.weights)
        self.biases -= learning_rate * np.sum(output_gradient, axis=0, keepdims=True)

        return input_gradient

    def get_params(self):
        return self.weights, self.biases

    def set_params(self, weights, biases):
        self.weights = weights
        self.biases = biases


class Activation(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_gradient, learning_rate, lambda_):
        return np.multiply(output_gradient, self.activation_prime(self.input))


class Tanh(Activation):
    def __init__(self):
        super().__init__(self.tanh, self.tanh_prime)

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def tanh_prime(x):
        return 1.0 - np.tanh(x) ** 2


class Trainer:
    def __init__(self, X, y, architecture, **params):
        self.X = X
        self.y = y
        self.epochs = params.get("epochs", 10000)
        self.learning_rate = params.get("learning_rate", 0.15)
        self.lambda_ = params.get("lambda_", 1e-5)
        self.tolerance = params.get("tolerance", 1e-5)
        self.prev_loss = params.get("prev_loss", None)

        self.network = []
        for layer in architecture:
            if layer["type"] == "Dense":
                self.network.append(Dense(layer["input_dim"], layer["output_dim"]))
            elif layer["type"] == "Tanh":
                self.network.append(Tanh())

    def run_training(self):
        for epoch in range(self.epochs):
            output = self.X
            for layer in self.network:
                output = layer.forward(output)

            # Extract weights for regularization from the Dense layers
            # and concatenate all the weights into one flat array
            weights = [
                layer.weights for layer in self.network if isinstance(layer, Dense)
            ]
            all_weights = np.concatenate([w.flatten() for w in weights])
            # Calculate loss with regularization
            loss = regularized_mse(self.y, output, all_weights, self.lambda_)

            # Check for early stopping
            if self.prev_loss is not None:
                if abs(self.prev_loss - loss) < self.tolerance:
                    logging.warning(f"Early stopping on epoch {epoch}, Loss: {loss}")
                    break

            # Backward pass
            gradient = mse_prime(self.y, output)
            for layer in reversed(self.network):
                gradient = layer.backward(gradient, self.learning_rate, self.lambda_)

            # Print loss every 1000 epochs
            if epoch % 1000 == 0:
                logging.info(f"Epoch {epoch}, Loss: {loss}")

            self.prev_loss = loss  # Update the previous loss

        # save the trained network as an attribute
        self.trained_network = self.network

    def save_model(self, filename):
        model_parameters = [
            layer.get_params()
            for layer in self.trained_network
            if isinstance(layer, Dense)
        ]
        np.save(filename, model_parameters)

    def load_model(self, filename):
        model_parameters = np.load(filename, allow_pickle=True)
        for layer, params in zip(self.network, model_parameters):
            if isinstance(layer, Dense):
                layer.set_params(*params)

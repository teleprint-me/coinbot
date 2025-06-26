"""
Copyright (C) 2023 - 2025 Austin Berrio
@file coinbot.model.dense
@brief A module for dense neural network models.
@license AGPL
@ref https://en.wikipedia.org/wiki/Feedforward_neural_network
"""

from abc import ABC, abstractmethod

import h5py
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


def rms(y_true, y_pred):
    return np.sqrt(np.mean(np.square(y_true - y_pred)))


def rms_prime(y_true, y_pred):
    return (y_pred - y_true) / (
        y_true.size * np.sqrt(np.mean(np.square(y_true - y_pred)))
    )


def regularized_rms(y_true, y_pred, weights, lambda_):
    rms_loss = np.sqrt(np.mean(np.square(y_true - y_pred)))
    l2_penalty = lambda_ * np.sum(np.square(weights))
    return rms_loss + l2_penalty


class Layer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def forward(self, input_data):
        pass

    @abstractmethod
    def backward(self, output_gradient, learning_rate):
        pass


class Dense(Layer):
    def __init__(self, input_dim, output_dim, seed=None, activation_fn=None):
        self.input_dim = input_dim
        self.output_dim = output_dim

        if seed is not None:
            np.random.seed(seed)

        self._initialize_weights(activation_fn)
        self.biases = np.zeros((1, output_dim))

    def _initialize_weights(self, activation_fn):
        if activation_fn == "relu":  # He Initialization - Var(W) = 1/n
            self.weights = np.random.randn(self.input_dim, self.output_dim) * np.sqrt(
                2.0 / self.input_dim
            )
        elif activation_fn in ["tanh", "sigmoid"]:
            # Xavier/Glorot Initialization - Var(W) = 2/n
            self.weights = np.random.randn(self.input_dim, self.output_dim) * np.sqrt(
                1.0 / self.input_dim
            )
        else:  # Fallback to random initialization
            self.weights = np.random.randn(self.input_dim, self.output_dim)

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

    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient, self.activation_prime(self.input))


class Sigmoid(Activation):
    def __init__(self):
        super().__init__(self.sigmoid, self.sigmoid_prime)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_prime(x):
        s = 1 / (1 + np.exp(-x))
        return s * (1 - s)


class ReLU(Activation):
    def __init__(self):
        super().__init__(self.relu, self.relu_prime)

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def relu_prime(x):
        return (x > 0).astype(float)


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
                if isinstance(layer, Dense):
                    gradient = layer.backward(
                        gradient, self.learning_rate, self.lambda_
                    )
                else:
                    gradient = layer.backward(gradient, self.learning_rate)

            # Print loss every 1000 epochs
            if epoch % 1000 == 0:
                logging.info(f"Epoch {epoch}, Loss: {loss}")

            self.prev_loss = loss  # Update the previous loss

        # save the trained network as an attribute
        self.trained_network = self.network

    def run_prediction(self, X):
        # Run a prediction with the model
        output = X
        for layer in self.trained_network:
            output = layer.forward(output)
        return output

    def get_metadata(self):
        metadata = []
        for layer in self.trained_network:
            layer_info = {"type": type(layer).__name__}
            if isinstance(layer, Dense):
                layer_info["input_dim"] = layer.weights.shape[0]
                layer_info["output_dim"] = layer.weights.shape[1]
            metadata.append(layer_info)
        return metadata

    def save_model(self, file_name):
        with h5py.File(file_name, "w") as hf:
            for i, layer in enumerate(self.trained_network):
                # Create a group for each layer
                # NOTE: This should cover up to a max of 999 layers.
                # I currently see no valid reason to go above 32 layers.
                # More neurons can be added per layer which can add up quickly.
                layer_group = hf.create_group(f"layer_{i:03}")

                if isinstance(layer, Dense):
                    # Store weights and biases as datasets within the group
                    layer_group.create_dataset("weights", data=layer.weights)
                    layer_group.create_dataset("biases", data=layer.biases)

                    # You can even store metadata as attributes
                    layer_group.attrs["type"] = "Dense"
                    layer_group.attrs["input_dim"] = layer.input_dim
                    layer_group.attrs["output_dim"] = layer.output_dim
                elif isinstance(layer, Activation):
                    # Mark the Activation functions position
                    layer_group.attrs["type"] = "Tanh"

    def load_model(self, file_name):
        trained_network = []
        with h5py.File(file_name, "r") as hf:
            for i, key in enumerate(hf.keys()):
                # Get the group from the files metadata
                layer_group = hf[key]

                # Read type and dimensions from attributes
                layer_type = layer_group.attrs["type"]

                if layer_type == "Dense":
                    # Get the Dense layer i/o dimensions
                    input_dim = layer_group.attrs["input_dim"]
                    output_dim = layer_group.attrs["output_dim"]

                    # Create a new Dense layer
                    layer = Dense(input_dim, output_dim)

                    # Populate its parameters
                    layer.weights = np.array(layer_group["weights"])
                    layer.biases = np.array(layer_group["biases"])
                elif layer_type == "Tanh":
                    # Create the Activation function
                    layer = Tanh()

                # Append to network
                trained_network.append(layer)

        self.trained_network = trained_network

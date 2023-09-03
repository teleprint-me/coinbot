"""
coinbot/model/dense.py
"""
from abc import abstractmethod

import numpy as np


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

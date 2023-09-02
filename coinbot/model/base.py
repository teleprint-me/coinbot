"""
coinbot/model/base.py
"""
from abc import abstractmethod


class Layer:
    def __init__(self):
        ...

    @abstractmethod
    def forward(self, input):
        ...

    @abstractmethod
    def backward(self, output_gradient, learning_rate):
        ...

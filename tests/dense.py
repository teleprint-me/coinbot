"""
tests/dense.py
"""
import numpy as np

from coinbot.model.dense import Dense, Tanh, mse, mse_prime


def test_initialization():
    layer = Dense(5, 3)
    assert layer.weights.shape == (5, 3)
    assert layer.biases.shape == (1, 3)


def test_forward_pass():
    layer = Dense(2, 1)
    layer.weights = np.array([[0.5], [0.5]])
    layer.biases = np.array([[0.5]])
    input_data = np.array([[2, 3]])

    output = layer.forward(input_data)
    assert np.allclose(output, np.array([[3.0]]))


def test_tanh_activation():
    layer = Tanh()
    output = layer.forward(np.array([-1.0, 0.0, 1.0]))
    assert np.allclose(output, np.array([-0.76159416, 0.0, 0.76159416]))


def test_mse_loss():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 4])
    loss = mse(y_true, y_pred)
    assert np.isclose(loss, 1 / 3)


def test_backward_pass():
    # Initialize layers
    dense1 = Dense(2, 3)
    activation1 = Tanh()
    dense2 = Dense(3, 1)
    activation2 = Tanh()

    # Initialize data
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = np.array([[0], [1], [1], [0]])

    # Forward pass
    layer1_output = dense1.forward(X)
    activation1_output = activation1.forward(layer1_output)
    layer2_output = dense2.forward(activation1_output)
    output = activation2.forward(layer2_output)

    # Compute loss and initial gradient
    loss = mse(Y, output)
    loss_gradient = mse_prime(Y, output)

    # Backward pass
    gradient = activation2.backward(loss_gradient, 0.1)
    gradient = dense2.backward(gradient, 0.1)
    gradient = activation1.backward(gradient, 0.1)
    gradient = dense1.backward(gradient, 0.1)

    # Assertions to verify the backward pass works as expected
    # Modify these as per your specific requirements
    assert loss >= 0  # Loss should be non-negative
    assert gradient.shape == X.shape  # Final gradient should have same shape as input

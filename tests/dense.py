"""
tests/dense.py
"""
import os

import h5py
import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from coinbot.model.dense import Dense, Tanh, Trainer, mse, mse_prime, regularized_mse


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


def test_regularized_mse():
    # Generate some random input and output data
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([0.8, 2.1, 3.2])

    # Generate some random weights
    weights = np.array([0.5, 0.4, 0.3])

    # Set regularization parameter
    lambda_ = 0.01

    # Calculate the mse loss without regularization
    mse_loss = mse(y_true, y_pred)

    # Calculate the regularized mse loss
    reg_mse_loss = regularized_mse(y_true, y_pred, weights, lambda_)

    # Manually calculate the regularization term
    l2_penalty = lambda_ * np.sum(np.square(weights))

    # Manually calculate the expected regularized mse loss
    expected_reg_mse_loss = mse_loss + l2_penalty

    # Verify if the function returns the expected regularized mse loss
    assert_almost_equal(reg_mse_loss, expected_reg_mse_loss, decimal=6)


def test_backward_pass():
    # Initialize layers
    dense1 = Dense(2, 3)
    activation1 = Tanh()
    dense2 = Dense(3, 1)
    activation2 = Tanh()

    # Initialize data
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = np.array([[0], [1], [1], [0]])

    # Store initial weights and biases for comparison
    initial_weights1 = dense1.weights.copy()
    initial_biases1 = dense1.biases.copy()
    initial_weights2 = dense2.weights.copy()
    initial_biases2 = dense2.biases.copy()

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
    gradient = dense2.backward(gradient, 0.1, 1e-5)
    gradient = activation1.backward(gradient, 0.1)
    gradient = dense1.backward(gradient, 0.1, 1e-5)

    # Assertions to verify the backward pass works as expected
    assert loss >= 0  # Loss should be non-negative
    assert (
        gradient.shape == X.shape
    )  # Final gradient should have the same shape as input

    # Check if weights and biases got updated
    assert not np.array_equal(initial_weights1, dense1.weights)
    assert not np.array_equal(initial_biases1, dense1.biases)
    assert not np.array_equal(initial_weights2, dense2.weights)
    assert not np.array_equal(initial_biases2, dense2.biases)


def test_trainer():
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

    # Perform training
    trainer.run_training()

    # Test the trained model
    output = trainer.run_prediction(X)

    # Thresholding to get binary output
    output = np.where(output >= 0.5, 1, 0)

    # Validate if the output matches expected values
    assert_almost_equal(output, y, decimal=1)

    # Save the model and check if it can be loaded
    filename = "test-model.h5"
    trainer.save_model(filename)

    # Check if HDF5 file exists
    assert os.path.exists(filename)

    # Check if the saved model can be loaded
    with h5py.File(filename, "r") as hf:
        assert "layer_000" in hf.keys()

    # Load the model using your function
    trainer.load_model(filename)

    # Re-run prediction to test if the loaded model works as expected
    output = trainer.run_prediction(X)
    output = np.where(output >= 0.5, 1, 0)

    # Validate if the output matches expected values
    assert_almost_equal(output, y, decimal=1)

    # Cleanup: Remove the test model file
    os.remove(filename)

# Investment Algorithm and Neural Network Model for Value Averaging Strategy

## Table of Contents

1. [Introduction](#Introduction)
2. [Background](#Background)
   - [Value Averaging Strategy](#Value-Averaging-Strategy)
   - [Mathematical Formulation](#Mathematical-Formulation)
3. [Objective](#Objective)
4. [Table Representation and Variables](#Table-Representation-and-Variables)
5. [Algorithm Development](#Algorithm-Development)
   - [Forward Pass Algorithm](#Forward-Pass-Algorithm)
6. [Neural Network Model](#Neural-Network-Model)
7. [Conclusion](#Conclusion)

## Introduction

In the realm of investment strategies, Value Averaging is a popular approach
aimed at optimizing portfolio value by adjusting investment amounts based on
real-time portfolio valuation. This project intends to deconstruct the strategy
into a sequence of mathematical functions. The objective is to formulate an
algorithm that can provide predictive insights into the Target Value based on
historical and current data.

## Background

### Value Averaging Strategy

Here, the concept behind the Value Averaging investment strategy will be
elucidated. This strategy is characterized by a tabulated sequence of steps,
each containing variables such as Market Price, Current Target, and Current
Value, among others.

### Mathematical Formulation

Understanding the algorithm from a mathematical standpoint is vital. The
variables and constants will be translated into mathematical expressions, laying
the foundation for algorithmic representation.

## Objective

The primary goal is to develop a forward-pass algorithm capable of estimating
the Target Value within a certain range, thereby aiding decision-making
processes in real-world investment scenarios.

## Mathematical Formulation of the Value Averaging Strategy

### Target Value Function \( T(i) \)

The Target Value \( T(i) \) is pivotal in implementing the Value Averaging
strategy. It's computed using the formula:

\[ T(i) = P \times i \times \left( 1 + \frac{r}{f} \right)^{i} \]

Where:

- \( P \) = Principal Amount
- \( r \) = Annual Interest Rate
- \( f \) = Frequency
- \( i \) = Current Interval

This formula encapsulates the compound growth based on the interest rate and the
frequency, making it the cornerstone of our algorithm. This ensures the target
amount is dynamic and reflects the time value of money.

### Predicting the Current Target

While \( T(i) \) is an independent variable calculated based on constant
parameters and the interval \( i \), predicting it would be straightforward if
these parameters are known. However, estimating \( T(i) \) relative to the
`Current Value` provides a dynamic range that can help in decision-making.

### Constraints and Thresholds

To prevent undesirably small trades, a `MIN_TRADE_AMOUNT` threshold can be
introduced into the algorithm. This will ensure that trades occur only when they
cross this minimum value, optimizing transaction costs and impact.

### Model Generalization to any given Asset

By recognizing that this strategy is applicable to any volatile, speculative
asset, we expand the scope and utility of our algorithm. This not only broadens
the appeal but also adds to its adaptability across different asset classes.

### Formalizing the Functions

#### 1. Target Value Function, \( T(i) \)

\[ T(i) = P \times i \times \left( 1 + \frac{r}{f} \right)^{i} \]

#### 2. Current Value Function, \( V(c) \)

\[ V(c) = M \times O\_{\text{prev}} \]

#### 3. Trade Amount Function, \( A(T, V) \)

\[ A(T, V) = T(i) - V(c) \]

This part is crucial because it transitions us from theoretical models to
actionable functions. Here we've precisely mapped out the relationship between
the Target Value \( T(i) \), Current Value \( V(c) \), and the Trade Amount \(
A(T, V) \).

### Predicting the Trade Amount \( A(T, V) \)

We've astutely noted that \( A(T, V) \) is a function of both \( T(i) \) and \(
V(c) \) and hinges on the predictability of these functions.

- \( T(i) \) can be determined algorithmically based on known variables.
- \( V(c) \), being market-dependent, presents more of a challenge.

For simulations or paper trading, employing historical data or educated guesses
for \( M \) (Market Price) can be a viable strategy for estimating \( V(c) \).

## Time Steps and Variables

The table keeps track of various parameters at each time step, such as:

- Datetime \( dt_t \)
- Market Price \( M_t \)
- Current Target \( T_t \)
- Current Value \( V_t \)
- And so on

### Table Representation

The table is used to represent a single investment within an investor's
portfolio, tracking the base and quote products for the trade pair.

| Exchange | Datetime | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |

### Visualizing Value Averaging Datasets

| Exchange | Date     | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| paper    | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 10.00        | 10.00              | 0.00107124 | 0.00107124       | 1        |
| paper    | 02/01/20 | 8,505.07     | 20.33          | 9.11          | 11.22        | 21.22              | 0.00131965 | 0.00239089       | 2        |
| paper    | 03/01/20 | 6,424.35     | 30.76          | 15.36         | 15.40        | 36.62              | 0.00239655 | 0.00478745       | 3        |
| paper    | 04/01/20 | 8,624.28     | 41.35          | 41.29         | 0.06         | 36.68              | 0.00000716 | 0.00479461       | 4        |
| paper    | 05/01/20 | 9,446.57     | 52.12          | 45.29         | 6.83         | 43.51              | 0.00072255 | 0.00551716       | 5        |

### Visualizing Sequencing and Time Series Data

| Exchange | Datetime | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| paper    | dt_i     | M_i          | T_i            | V_i           | A_i          | TA_i               | O_i        | TO_i             | i        |
| paper    | dt_i     | M_i          | T_i            | V_i           | A_i          | TA_i               | O_i        | TO_i             | i + 1    |
| paper    | dt_i     | M_i          | T_i            | V_i           | A_i          | TA_i               | O_i        | TO_i             | i + 1    |
| paper    | dt_i     | M_i          | T_i            | V_i           | A_i          | TA_i               | O_i        | TO_i             | i + 1    |
| paper    | dt_i     | M_i          | T_i            | V_i           | A_i          | TA_i               | O_i        | TO_i             | i + 1    |

### Updating and Improving the Value Averaging Model

\[ I(n) = n + 1 \]

In the context of a simulation, the Interval function \( I(n) \) generates the
linear sequence \( n \), essentially marking each interval \( i \) in the time
range. This adds a layer of temporal structure, making the simulation more
nuanced and providing a robust platform for performance evaluation.

### Updated Current Value Function with Market Price

\[ V(c) = M_i \times O\_{\text{prev}} \]

\[ I(n) = n + 1 \]

\[ I(n) \] is used in this section to determine the \( i \)-th interval, where
\( i = I(n) \), thus influencing \( M_i \) and ultimately \( V(c) \).

### Simulation Steps for \( A(T, V) \)

1. **Initialize \( n \)**: Set \( n = 0 \).
2. **Calculate \( i \)**: \( i = I(n) \).
3. **Fetch \( M_i \)**: From the time series based on \( i \).
4. **Calculate \( T(i) \)**: Utilizing your Target Value Function.
5. **Calculate \( V(c) \)**: With \( M_i \).
6. **Calculate \( A(T, V) \)**: \( T(i) - V(c) \).
7. **Update \( n \)**: \( n = n + 1 \).

### How to Interpret Each Variable

- \( dt_i \): Datetime at interval \( i \), influenced by \( I(n) \).
- \( M_i \): Market price at \( I(n) \).
- \( T_i \): Target value at \( I(n) \).
- \( V_i \): Current asset value at \( I(n) \).
- \( A_i \): Trade Amount at \( I(n) \).
- \( TA_i \): Cumulative trade amount up to \( I(n) \).
- \( O_i \): Order size at \( I(n) \).
- \( TO_i \): Cumulative order size up to \( I(n) \).

In this refined version, the function \( I(n) = n + 1 \) serves to produce the
linear sequencing of intervals \( i \). This function is critical for advancing
the time steps and influencing each variable in the simulation.

**Note**: `Datetime` is a timestamp marking when a record was created, whereas
the `Interval` progresses linearly and is governed by the function `I(n)=n+1`.

### Explicit Time Series Representation

To unambiguously define time steps in the model, let's introduce a new variable
\( n \). This variable will serve as the explicit representation of time steps
or intervals, independent of other variables.

In this revised model, the function for calculating the target value can be
represented as:

\[ T(n) = P \times n \times \left(1 + \frac{r}{f}\right)^n \]

Here, \( n \) is the clear indicator of the time step, enhancing model
interpretability.

Similarly, we can denote variables that are time-step specific but not
necessarily functions of time as \( M(n) \). This clarifies that they relate to
a given time step \( n \), without implying they are dependent on \( n \).

### Vectorization and Algorithmic Interpretation

Each column in the table can be conceptualized as a vector containing a sequence
of values over multiple time steps. For instance, the "Market Price" column \(
\mathbf{M(n)} \) can be viewed as a vector where each entry \( M(n) \)
represents the market price at the corresponding time step \( n \).

In the same vein, the "Current Target" column \( \mathbf{T(n)} \), "Current
Value" column \( \mathbf{V(n)} \), and other columns can also be considered as
vectors.

Understanding these columns as vectors opens up avenues for streamlined data
manipulation and analysis. This is particularly useful if we aim to implement
the model programmatically, allowing for more efficient algorithms and easier
debugging.

## Neural Network Model for Trading Predictions

Given that each row in the table encapsulates a feature vector for a particular
time step, we can train a neural network model to predict variables like the
next Target Value. Depending on the specific use-cases and data characteristics,
various neural network architectures such as Recurrent Neural Networks (RNNs),
Long Short-Term Memory networks (LSTMs), or Convolutional Neural Networks (CNNs)
may be applicable.

### Utilizing Recurrent and Convolutional Approaches for Enhanced Generalization

The inherent time-series structure of our trading data makes it amenable to
neural network modeling. If we represent the variables at each time step as
feature vectors, the neural network can effectively learn the intricate
relationships among these variables over sequential time frames. This capability
could be especially valuable for predicting the Target Value using historical
data.

Consider the following feature variables at each time step \( t \):

- "Market Price" \( M_t \)
- "Current Target" \( T_t \)
- "Current Value" \( V_t \)
- "Trade Amount" \( A_t \)
- And other relevant variables

We can combine these into a feature vector \( \mathbf{F_t} = [M\_t, T\_t, V\_t,
A\_t, \ldots] \) for each time step \( t \).

In architectures like RNNs or LSTMs, each feature vector \( \mathbf{F_t} \)
serves as the input for time step \( t \), allowing the model to be trained to
predict the subsequent target \( T\_{t+1} \). Convolutional layers could also be
introduced to capture local patterns in sequences of \( \mathbf{F_t} \),
assuming such patterns are pertinent.

Because our data is fundamentally time-series in nature, sequence-modeling
architectures like RNNs, LSTMs, and 1D convolutional layers are especially
suitable.

By simulating the Value Averaging investment strategy across a predefined
period, each iteration provides a computed `Trade Amount (A(T, V))`. This amount
specifies the investment needed to align your portfolio's `Current Value` with
the `Current Target` for that particular time step. This structured approach
offers the advantage of back-testing your investment strategy against historical
data, providing valuable insights into its prospective performance and
associated risks.

### Neural Network Model Planning and Outline

A neural network model can be invaluable for optimizing trading decisions,
particularly in volatile and unpredictable market conditions. Below is an
outline detailing key considerations for building such a model.

#### Architecture

1. **Input Layer**: Incorporate features like historical market prices,
   calculated `Current Value`, `Current Target`, and potentially macroeconomic
   indicators for a more holistic model.
2. **Hidden Layers**: The number and complexity of hidden layers should
   correspond to the complexity of your problem and the dataset size. Activation
   functions such as ReLU or Tanh may prove effective.

3. **Output Layer**: A single-neuron output layer can be employed for predicting
   the `Trade Amount` or `Order Size`.

#### Data Preparation

1. **Feature Scaling**: Employ normalization or standardization techniques on
   your input features to improve model efficiency.

2. **Data Splitting**: Divide your dataset into training, validation, and test
   subsets for a more robust evaluation.

3. **Sequencing**: For time-series models like LSTMs, prepare sequences of data
   points as input.

#### Training and Evaluation

1. **Loss Function**: Given the regression nature of the problem, loss functions
   like Mean Squared Error (MSE) or Mean Absolute Error (MAE) are appropriate.

2. **Optimizer**: Algorithms like Adam or RMSprop are recommended for this
   problem.

3. **Evaluation Metrics**: Use R2 Score, MAE, or Root Mean Squared Error (RMSE)
   to gauge model efficacy.

4. **Hyperparameter Tuning**: Leverage grid search or other optimization methods
   to fine-tune model hyperparameters.

#### Implementation

Utilize Python frameworks like TensorFlow or PyTorch for implementation. Given
your experience in Python, this aspect should be straightforward. For
performance optimization, you might find specialized libraries like `ggml`
useful, albeit requiring customization for financial modeling.

#### Post-Training Analysis

Once our model is trained, assess its performance using the test dataset.
Compare the predicted outputs with actual data to identify areas for improvement
and subsequent iterations.

### Neural Network Considerations

Representing each row as an independent feature vector allows you to handle each
time step as a unique input. We can then feed these vectors into the neural
network in batches or sequences, depending on the architecture we're
considering. Here are a few paths we could take:

1. **Feed-forward Neural Network (DNN)**: Use each vector independently to
   predict the next time step's target. This won't capture the sequential nature
   but could serve as a baseline model.

2. **Recurrent Neural Networks (RNN)**: Use the sequence of vectors to take into
   account the temporal dependencies between different time steps. The state of
   the network is updated as each new vector is fed into the model, and this
   state serves as a form of memory.

3. **Long Short-Term Memory (LSTM)**: Similar to RNNs but better at capturing
   long-term dependencies, making them often more suitable for financial
   time-series prediction.

4. **Convolutional Neural Networks (CNN)**: While commonly used for image data,
   1D convolutions could capture local patterns within a sequence of vectors.
   You might stack these with RNN or LSTM layers for capturing both local and
   global patterns.

5. **Transformer-based models**: These are particularly effective if you're
   dealing with sequences and have become very popular for a variety of tasks.
   The attention mechanism would allow the model to focus on different parts of
   the input sequence when making predictions.

6. **Hybrid Models**: Combinations of the above, perhaps a CNN for capturing
   local patterns in the short term, followed by an LSTM for long-term
   dependencies.

7. **Reinforcement Learning**: This is more complex but could be very suitable
   for trading problems. You'd treat each trading decision as an action, and the
   reward would be the profit or loss.

## Starting with a Dense Neural Network: Hello World!

Starting with a Dense Neural Network (DNN) for a proof-of-concept seems like the
most sensible approach. It allows for a simpler architecture while providing a
baseline model that you can compare more complex architectures against later on.

Here's a general outline for each step:

### 1. Implementation Design

We could go with a Keras-like API design, where you instantiate layers and stack
them. Given that you're experienced in Python and software development, this
might be a good way to structure your code.

### 2. Create the Base Layer

The base layer would handle initialization of weights and biases, along with
some utility methods like `forward` and `backward` for propagation. These are
common among all types of layers.

### 3. Create the Dense Layer

A dense layer would inherit from the base layer and implement the specific logic
for forward and backward propagation for fully connected layers.

### 4. Create the Activation Layer

Same as the dense layer but for activation functions like ReLU, Sigmoid, or
Softmax.

### 5. Implement Activation and Loss Functions

We'd have separate modules for activation functions (ReLU, Sigmoid, Softmax) and
loss functions (Mean Squared Error, Cross-Entropy).

### 6. Solve XOR (MNIST)

Starting with XOR is a great idea because it's the "Hello, World!" of neural
networks. We can then scale up from there.

### Data Structure

```py
data = [
    ["Exchange", "Date", "Market Price", "Current Target", "Current Value", "Trade Amount", "Total Trade Amount", "Order Size", "Total Order Size", "Interval"],
    ["paper", "01/01/20", 9334.98, 10.00, 0.00, 10.00, 10.00, 0.00107124, 0.00107124, 1],
    ["paper", "02/01/20", 8505.07, 20.33, 9.11, 11.22, 21.22, 0.00131965, 0.00239089, 2],
    ["paper", "03/01/20", 6424.35, 30.76, 15.36, 15.40, 36.62, 0.00239655, 0.00478745, 3],
    ["paper", "04/01/20", 8624.28, 41.35, 41.29, 0.06, 36.68, 0.00000716, 0.00479461, 4],
    ["paper", "05/01/20", 9446.57, 52.12, 45.29, 6.83, 43.51, 0.00072255, 0.00551716, 5],
    ["paper", "06/01/20", 9136.20, 63.06, 50.41, 12.66, 56.16, 0.00138539, 0.00690255, 6],
    ["paper", "07/01/20", 11351.62, 74.19, 78.36, -4.17, 52.00, -0.00036721, 0.00653534, 7],
    ["paper", "08/01/20", 11655.00, 85.49, 76.17, 9.32, 61.32, 0.00079982, 0.00733516, 8],
    ["paper", "09/01/20", 10779.63, 96.98, 79.07, 17.91, 79.23, 0.00166136, 0.00899652, 9],
    ["paper", "10/01/20", 13804.81, 108.65, 124.20, -15.54, 63.68, -0.00112589, 0.00787063, 10],
    ["paper", "11/01/20", 19713.94, 120.51, 155.16, -34.65, 29.04, -0.00175751, 0.00611312, 11],
    ["paper", "12/01/20", 28990.08, 132.57, 177.22, -44.65, -15.62, -0.00154035, 0.00457277, 12]
]
```

The `data` list we provided can serve as a straightforward way to input data
into the neural network. We'd likely want to preprocess this data into NumPy
arrays or tensors (if using PyTorch). We might also want to normalize some of
these columns so they are in similar scales, making it easier for the network to
learn.

We could convert the input features and labels into tensors and proceed with
training and validation.

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

## Table Representation

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

When operating within a simulation framework, leveraging historical closing
prices from a time series dataset is an effective approach for setting the
Market Price \( M \). This not only enriches the simulation's realism but also
offers a versatile platform for performance evaluation under diverse market
conditions.

### Updated Current Value Function with Market Price

To better adapt your Current Value Function \( V(c) \) in a simulation, the
equation can be modified as:

\[ V(c) = M*i \times O*{\text{prev}} \]

Here \( M*i \) represents the market price at the \( i \)-th interval, which can
be fetched from the historical closing prices in your time series dataset. \(
O*{\text{prev}} \) is the accumulated sum of all previous order sizes, aligning
with your primary algorithmic approach.

### Simulation Steps for \( A(T, V) \)

For each interval \( i \) in your time range, the following steps can be looped:

1. **Fetch \( M_i \)**: Retrieve the market price at the current interval \( i
   \) from the time series.
2. **Calculate \( T(i) \)**: Utilize your previously defined Target Value
   Function.
3. **Calculate \( V(c) \)**: Implement the updated Current Value Function with
   \( M_i \).
4. **Calculate \( A(T, V) \)**: Compute as \( T(i) - V(c) \).

This iterative process generates a series of \( A(T, V) \), allowing you to
simulate Trade Amounts at every step.

### How to Interpret Each Variable

The use of symbolic notation efficiently abstracts the underlying mechanics of
each table column. This not only aids in visualizing the data flow but also in
comprehending how variables evolve at each interval \( i \).

Here’s a concise variable breakdown:

- \( dt_i \): Datetime for record-keeping at interval \( i \).
- \( M_i \): Market price fetched at the \( i \)-th interval.
- \( T_i \): Target value, computed using your defined function at interval \( i
  \).
- \( V_i \): Current asset value at interval \( i \).
- \( A_i \): Trade Amount, a function of \( T_i \) and \( V_i \), calculated as
  \( A(T, V) = T - V \).
- \( TA_i \): Cumulative trade amount up to interval \( i \), essentially the
  running sum of \( A_i \).
- \( O_i \): Order size at interval \( i \), derived from \( A_i \) and \( M_i
  \).
- \( TO_i \): Cumulative order size up to interval \( i \), another running sum
  but of \( O_i \).

The usage of \( i \) to signify time steps accentuates the temporal dependencies
and offers a snapshot of the system's state at each specific \( i \).

### Accurately representing time series representations

Introducing a different variable to explicitly denote the time step could indeed
reduce confusion.

Let's say we introduce a new variable \( n \) to represent the time step or
interval, separate from any other variables. The function for calculating the
target could then be written as:

\[ T(n) = P \times n \times (1 + \frac{r}{f})^n \]

This way, \( n \) serves as an explicit indicator of the time step.

Similarly, for other variables that depend on the time step but are not
explicitly a function of it, like \( M \), we can represent them as \( M(n) \)
to clarify that they are specific to a given time step \( n \) but not dependent
variables of \( n \).

### Considerations for vectorization and model interpretation and prediction

Each column in the table can be viewed as a vector that holds a sequence of
values over multiple time steps. For example, the "Market Price" column \(
\mathbf{M(n)} \) is a vector where each entry \( M(n) \) corresponds to the
market price at time step \( n \).

Similarly, the "Current Target" column \( \mathbf{T(n)} \), "Current Value"
column \( \mathbf{V(n)} \), and others can be viewed as vectors in the same
manner.

Understanding them as vectors could make it easier to manipulate and analyze the
data, especially if you're planning to implement the algorithm programmatically.
Would you like to explore this further?

## Neural Network Model

Given that each row in the table is essentially a feature vector, a neural
network can be trained to predict the next Target Value or other relevant
variables. Different architectures such as RNNs, LSTMs, or CNNs may be
applicable depending on the specific requirements.

### Utilization Analog and Convolutional approaches for generalization

The structure of your trading data can lend itself well to a neural network
approach. If you can represent the variables in each time step as feature
vectors, then a neural network can learn the underlying relationships between
these variables over time. This could be particularly useful for predicting the
Target Value based on prior information.

Let's consider the following:

- The "Market Price" at each time step can be a feature \( M_t \)
- The "Current Target" at each time step \( T_t \)
- The "Current Value" \( V_t \)
- The "Trade Amount" \( A_t \)
- And so on for other variables.

These can be combined into a feature vector \( \mathbf{F_t} = [M_t, T_t, V_t,
A_t, \ldots] \) for each time step \( t \).

If you're using a recurrent neural network (RNN) or LSTM, each \( \mathbf{F*t}
\) could be input at each time step \( t \), and the network could then be
trained to predict the next \( T*{t+1} \), for example. Convolutional layers
could be useful for capturing local patterns in sequences of \( \mathbf{F_t} \),
if you think such patterns might be relevant.

In your case, the data is essentially time-series data, so the kind of network
architectures that are commonly used for sequence modeling might be particularly
applicable. These include RNNs, LSTMs, or even 1D convolutional layers for
capturing local patterns.

You'll be able to simulate the Value Averaging investment strategy over a set
period. Each loop iteration will provide you with a calculated
`Trade Amount (A(T, V))` that reflects how much you should invest to bring your
portfolio's `Current Value` closer to the `Current Target` for that time step.
This systematic approach enables you to test your investment strategy against
historical market data, giving you insights into its potential performance and
risk profile.

### Neural Network Model Planning and Outline

A neural network could potentially help in fine-tuning your trade decisions,
especially when market conditions are volatile and hard to predict.

Here are some ideas for the Neural Network model:

### Architecture

1. **Input Layer**: Features could include historical market prices, calculated
   `Current Value`, `Current Target`, and perhaps even macroeconomic indicators.

2. **Hidden Layers**: Depending on the complexity of the problem and the amount
   of data you have, you could have multiple layers. Activation functions like
   ReLU or Tanh could be beneficial.

3. **Output Layer**: A single neuron that predicts the `Trade Amount` or the
   `Order Size`.

### Data Preparation

1. **Feature Scaling**: Normalize or standardize the input features for better
   model performance.

2. **Data Split**: Partition the data into training, validation, and test sets.

3. **Sequencing**: If you decide to use a time series model like LSTM, you'll
   need to create sequences of data as input.

### Training and Evaluation

1. **Loss Function**: Since this is a regression problem, you could use loss
   functions like MSE or MAE.

2. **Optimizer**: Adam or RMSprop could be good choices for this problem.

3. **Evaluation Metrics**: Consider using R2 Score, MAE, or RMSE for evaluating
   the model performance.

4. **Hyperparameter Tuning**: Perform a grid search or use other techniques to
   find optimal hyperparameters.

### Implementation

You could implement this in Python using TensorFlow or PyTorch. Since you have
experience with Python, the coding part should be within your wheelhouse. If
you're interested in performance optimization, libraries like `ggml` might be of
interest, although they might require some adaptation for financial modeling.

### Post-Training

After training, evaluate your model using your test set and compare the
predictions with the actual outcomes. You can then refine your model based on
the insights you gain.

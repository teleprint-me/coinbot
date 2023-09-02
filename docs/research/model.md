# Investment Simulation Algorithm and Neural Network Model

## Table of Contents
1. [Algorithm Overview](#Algorithm-Overview)
2. [Target Value Function](#Target-Value-Function)
3. [Time Steps and Variables](#Time-Steps-and-Variables)
4. [Table Representation](#Table-Representation)
5. [Neural Network Model](#Neural-Network-Model)

## Algorithm Overview

1. Define Principal Amount
2. Define Annual Interest Rate
3. Define Frequency
4. Define Time Period
5. Get Datetime
6. Get Market Price
7. Get Interval
8. Get Current Target
9. Get Previous Total Order Size
10. Get Order Size
11. Get Total Order Size
12. Get Current Value
13. Get Previous Total Trade Amount
14. Get Trade Amount
15. Get Total Trade Amount

## Target Value Function

The Target Value is calculated as follows:

\[ T(i) = P \times i \times (1 + \frac{r}{f})^i \]

Where \( P \) is the principal amount, \( r \) is the annual interest rate, \( f \) is the frequency, and \( i \) is the interval.

## Time Steps and Variables

The table keeps track of various parameters at each time step, such as:

- Datetime \( dt_t \)
- Market Price \( M_t \)
- Current Target \( T_t \)
- Current Value \( V_t \)
- And so on

## Table Representation

The table is used to represent a single investment within an investor's portfolio, tracking the base and quote products for the trade pair.

| Exchange | Datetime | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |

## Neural Network Model

Given that each row in the table is essentially a feature vector, a neural network can be trained to predict the next Target Value or other relevant variables. Different architectures such as RNNs, LSTMs, or CNNs may be applicable depending on the specific requirements.

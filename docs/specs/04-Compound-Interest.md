## Compound Interest Formula

The compound interest formula is traditionally used to calculate the future
value of an investment or loan. In trading strategies like Value Averaging, a
modified version of the formula can be used to determine the target amount for a
given trade. The standard formula is:

```
A = P * (1 + (r / n))^(nt)
```

Where:

- `A` is the accumulated amount money over `n` years, including interest.
- `P` is the principal amount or the initial investment.
- `r` is the annual interest rate in decimal form.
- `n` is the number of times interest is compounded per unit `t`.
- `t` is the time in years the money is invested or borrowed.

## Compound Interest in Value Averaging

In the context of Value Averaging, the compound interest formula can be adapted
to meet specific trading objectives. We explored different variations to tailor
the formula for this strategy.

### Formula Variations

1. **Original Formula**: Initially, we used this formula to strictly follow the
   compound interest model, aiming for exponential growth. However, we found
   that it could be simplified for practical implementation.

   ```
   Accumulated Amount = Principal Amount * (1 + (Annual Interest Rate / Frequency))^(Frequency * Time Period * Interval)
   ```

2. **Simplified Formula**: This adapted formula incorporates the concept of
   "Interval," unique to Value Averaging. The "Interval" represents the time
   step in the sequence of investments. This formula effectively captures both
   linear and compound growth factors.

   ```
   Current Target = Principal Amount * Interval * (1 + (Annual Interest Rate / Frequency))^Interval
   ```

### Calculating the Trade Amount

The trade amount needed to reach the target investment is calculated as follows:

```
Trade Amount = Current Target - Current Value
```

## Formula Parameters

1. **Principal Amount (`P`)**: This is the initial investment or the amount you
   aim to invest at each step.
2. **Annual Interest Rate (`r`)**: Represents the average annual percentage gain
   you aim to achieve through trading.
3. **Compounding Frequency (`n`)**: Specifies how often you intend to trade,
   e.g., 365 for daily trades.
4. **Time Period (`t`)**: The length of time, usually in years, for which the
   investment is held. This can be adjusted to fit your trading strategy.
5. **Interval (`i`)**: This is unique to Value Averaging and represents the time
   step in the sequence. It influences the "Current Target", essentially scaling
   the principal investment to account for the chosen interval. This is
   important because the Value Averaging strategy involves making regular
   contributions or adjustments to the investment to bring it in line with the
   desired growth trajectory.

### Implementation Steps

The chosen formula can be implemented in your preferred programming language.
The trade amount is computed as the difference between the calculated "Current
Target" and your current asset value in the chosen trading pair (e.g., BTC,
ETH).

## Summary

**Compound Interest Formula**

```
A = P * (1 + (r / n))^(nt)
```

**Value Averaging Formula**

```
T = P * i * (1 + (r / n))^(i)
```

Where:

- **Compound Interest Formula (`A`)** calculates the accumulated amount of money
  over `n` years, accounting for interest.
- **Value Averaging Formula (`T`)** calculates the Current Target amount
  accumulated over `i` intervals, accounting for interest. This formula is
  specific to the Value Averaging strategy.
- **Principal (`P`)** is the initial investment amount.
- **Annual Interest Rate (`r`)** is the interest rate in decimal form.
- **Compounding Frequency (`n`)** is how often interest is compounded per unit
  `t`.
- **Time Period (`t`)** is the time in years for the investment.
- **Interval (`i`)** is the unique time step in Value Averaging strategies,
  representing the duration between each trading or adjustment action.

In the Value Averaging Formula, multiplying the interval `i` with the principal
amount `P` adjusts the initial investment to account for the chosen interval.
This adjustment ensures the investment gradually approaches the desired target
amount over each interval, aligning with the Value Averaging strategy's growth
objective.

**Note**: While the compound interest formula focuses on the long-term
accumulation of an amount, the Value Averaging strategy aims to achieve a
specific Current Target at each interval, considering both linear and compound
growth factors.

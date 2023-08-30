## Compound Interest Formula

The compound interest formula is used to calculate the target amount for a given
trade. The formula is as follows:

```
A = P(1 + (r/n))^(nt)
```

Where:

- `P` is the principal amount (initial investment)
- `r` is the annual interest rate (in decimal form)
- `n` is the number of times that interest is compounded per unit `t`
- `t` is the time the money is invested/borrowed for, in years

## Compound Interest Formula in Value Averaging

The compound interest formula serves as the base for calculating the target
amount in Value Averaging trading strategies. The general compound interest
formula is:

```
A = P(1 + (r/n))^(nt)
```

However, in the context of Value Averaging, there may be different adaptations
of this formula to meet specific trading needs.

### Formula Variations

1. **Original Formula**: This formula incorporates the concept of "Interval,"
   which is unique to the Value Averaging strategy. The "Interval" signifies the
   time step in the investment sequence.

   ```
   Current Target = Principal Amount * Interval * (1 + (Annual Interest Rate / Frequency))^Interval
   ```

2. **Modified Formula with Compound Interest**: This formula aims to strictly
   follow the compound interest model for exponential growth.

   ```
   Current Target = Principal Amount * (1 + (Annual Interest Rate / Frequency))^(Frequency * Time Period * Interval)
   ```

3. **Simplified Formula**: This formula is a blend of the two, combining both
   linear and compound growth.

   ```
   Current Target = Principal Amount * Interval * (1 + (Annual Interest Rate / Frequency))^(Frequency * Time Period)
   ```

### Calculating Trade Amount

The trade amount is calculated using the formula:

```
Trade Amount = Current Target - Current Value
```

This gives the amount you need to buy or sell to reach your target investment
amount.

## Formula Parameters

1. **Principal Amount (`P`)**: The initial investment amount, or the amount of
   asset you aim to invest.
2. **Annual Interest Rate (`r`)**: Represents the average percentage gain you
   aim to achieve through trading.
3. **Compounding Frequency (`n`)**: Indicates how often you plan to execute
   trades (e.g., 365 for daily trades).
4. **Time Period (`t`)**: The time the investment is held, usually in years, but
   can be adjusted to match your trading strategy.
5. **Interval**: Unique to Value Averaging, this represents the time step in the
   sequence and influences the Current Target.

### Implementation

You can implement the chosen formula in your preferred programming language. The
trade amount is the difference between your calculated "Current Target" and your
current asset value in the trading pair (e.g., BTC, ETH).

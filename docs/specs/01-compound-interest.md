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

### Calculating Trade Amount

The trade amount is calculated using the formula:

```
Trade Amount = A - Current Value
```

## Formula Parameters

1. **Principal Amount (`P`)**: The amount of asset you currently have in the
   trading pair (BTC or ETH).

2. **Annual Interest Rate (`r`)**: This represents the average percentage gain
   you aim to achieve through trading.

3. **Compounding Frequency (`n`)**: This depends on how often you plan to
   execute trades. For example, if you plan to trade once a day, `n` would
   be 365.

4. **Time Period (`t`)**: The time the investment/borrowing is held, usually in
   years. You can adjust it to match your trading strategy.

### Implementation

To calculate the target amount (`A`) and subsequently the trade amount, you can
use the compound interest formula provided above. Implement this in your chosen
programming language, such as Python or another suitable language.

Remember that the trade amount is the difference between the calculated target
amount and your current asset value in either BTC or ETH.

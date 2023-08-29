**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research.**_

# Dynamic Cost Averaging

Dynamic Cost Averaging (DCA) is a variation of Cost Averaging that encourages
both buying and selling. Like Cost Averaging, DCA involves setting a Principal
Amount and purchasing an asset at a regular interval, called the Interval.
However, DCA also includes selling assets when certain conditions are met.

In DCA, a Target Value helps determine the amount to buy or sell based on a
Multiplier of the Principal Amount. This Multiplier falls within a range defined
by the Min Multiplier and Max Multiplier. These factors and variables can be
customized by the user. Let's briefly describe each term:

-   Principal Amount: The initial investment or the base amount for purchasing
    the asset.
-   Interval: The regular interval at which the asset is bought or sold.
-   Target Value: A predefined value that helps determine when to buy or sell.
-   Multiplier: A multiplier applied to the Principal Amount to calculate the
    buying or selling amount.
-   Min Multiplier and Max Multiplier: The lower and upper bounds of the
    Multiplier range, respectively.

## Dynamic Cost Averaging Algorithm

We need to define our columns: Datetime, Market Price, Current Target, Current
Value, Principal Amount, Multiplier, Trade Amount, Total Trade Amount, Order
Size, Total Order Size, and Interval. This will allow us to keep track of the
relevant data and show the evaluated expressions as its set of results.

We define the sequence of steps, as well as the expressions used, to evaluate
each value as the following:

1.  Define Principal Amount

        Principal Amount = Constant Float Value

2.  Define Multiplier Range

        Min Multiplier = 1 (sets lower limit)
        Max Multiplier = Constant Integer Value greater than Min Multiplier sets upper limit (default is 5)

3.  Get the current Datetime

        Datetime = Current Date

4.  Get the current Market Price

        Market Price = Current Market Price

5.  Set or calculate the Interval

        IF no previous records
            THEN Interval = 1
        ELSE
            Interval = Previous Record Interval + 1

6.  Calculate the Current Target

        Current Target = Principal Amount * Interval

7.  Set or calculate the Previous Total Order Size

        IF no previous records
            THEN Previous Total Order Size = 0
        ELSE
            Previous Total Order Size = sum of Order Size column for all previous records

8.  Get or calculate Order Size

        Order Size = Principal Amount / Market Price

9.  Calculate the Total Order Size

        Total Order Size = Order Size + Previous Total Order Size

10. Get or calculate the Current Value

        Current Value = Market Price * Previous Total Order Size

11. Calculate the Multiplier

    Determine how much should be bought or sold to get back to the Target Value.

        Target Difference = Current Target - Current Value
        Target Difference = 10 - 0 = 10

    Multiplier represents a value that is used to determine the size of the next
    trade.

        Multiplier = Target Difference / Principal Amount
        Multiplier = 10 / 10 = 1

    Enforce the Min Multiplier and Max Multiplier limits.

        IF Multiplier = 0
            THEN Multiplier = 1
        ELSE IF Multiplier > Max Multiplier
            THEN Multiplier = Max Multiplier
        ELSE IF Multiplier < -Max Multiplier
            THEN Multiplier = -Max Multiplier
        ELSE IF Multiplier < 0
            THEN Multiplier = -round(max(Min Multiplier, min(Multiplier, Max Multiplier)))
        ELSE
            Multiplier = round(max(Min Multiplier, min(Multiplier, Max Multiplier)))

    In this case, the Multiplier is within the limits:

        Multiplier = 1

12. Calculate the Trade Amount

        Trade Amount = Multiplier * Principal Amount

13. Get or calculate Previous Total Trade Amount

        IF no previous records
            THEN Previous Total Trade Amount = 0
        ELSE
            Previous Total Trade Amount = sum of Trade Amount column for all previous records

14. Calculate the Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount

15. Update Previous Total Trade Amount and Previous Total Order Size

        Previous Total Trade Amount = Total Trade Amount
        Previous Total Order Size = Total Order Size

## Dynamic Cost Averaging Walk-through

I want to paper trade a Value Averaging strategy, investing $10 per month in the
BTC-USD trading pair over a 1-year period. I will make the investments on the
first day of each month in 2020.

-   The smallest units for US dollars are denominated in "cents" and will use a
    precision of:

        1 * 10 ^ -2 = 0.01

-   The smallest units for Bitcoin are denominated in "satoshis" and will use a
    precision of:

        1 * 10 ^ -8 = 0.00000001

### Creating the Initial Record

Let's initialize the table and calculate the first record:

1.  Initialize Interval, Previous Total Order Size, and Previous Total Trade
    Amount. There are no previous records and we set the following variables as
    a result. This omits steps 5 (Set or Calculate Interval), 7 (Set or
    Calculate Previous Total Order Size), and step 13 (Get Previous Total Trade
    Amount).

        Interval = 1
        Previous Total Order Size = 0
        Previous Total Trade Amount = 0

2.  Define the Multiplier Range for the algorithm

        Min Multiplier = 1 (sets lower limit)
        Max Multiplier = Constant Integer Value greater than Min Multiplier sets upper limit (default is 5)

        Min Multiplier = 1
        Max Multiplier = 5

3.  Set the Principal Amount for the investment

        Principal Amount = Constant Float Value
        Principal Amount = 10.00

4.  Initialize Datetime with the date of the first record

        Datetime = Current Date
        Datetime = "2020-01-01"

5.  Get the Market Price for the first record

        Market Price = Current Market Price
        Market Price = 9334.98

6.  Calculate the Current Target

        Current Target = Principal Amount * Interval
        Current Target = 10 * 1 = 10

7.  Calculate or get the Order Size

        Order Size = Principal Amount / Market Price
        Order Size = 10 / 9334.98 ≈ 0.0010712395741608446 ≈ 0.00107124

8.  Calculate the Total Order Size

        Total Order Size = Order Size + Previous Total Order Size
        Total Order Size = 0.00107124 + 0 = 0.00107124

9.  Calculate the Current Value

        Current Value = Market Price * Previous Total Order Size
        Current Value = 9334.98 * 0 = 0

10. Calculate the Multiplier

    Determine how much should be bought or sold to get back to the Target Value.

        Target Difference = Current Target - Current Value Target Difference
        Target Difference = 10 - 0 = 10

    Multiplier represents a value that is used to determine the size of the next
    trade.

        Multiplier = Target Difference / Principal Amount
        Multiplier = 10 / 10 = 1

    Enforce the Min Multiplier and Max Multiplier limits.

        IF Multiplier = 0
            THEN RETURN 1
        IF Multiplier > Max Multiplier
            THEN RETURN Max Multiplier
        IF Multiplier < -Max Multiplier
            THEN RETURN -Max Multiplier
        RETURN max(Min Multiplier, min(Multiplier, Max Multiplier))

    In this case, the Multiplier is within the limits:

        Multiplier = 1

11. Calculate the Trade Amount

        Trade Amount = Multiplier * Principal Amount
        Trade Amount = 1 * 10 = 10

    -   Example of how to calculate Target Difference, Multiplier, and Trade
        Amount to buy:

            Target Difference = 20 - 9.11 = 10.89 (positive value is a buy signal)
            Multiplier = 10.89 / 10 ≈ 1.09 ≈ 1 (rounded to the nearest integer)
            Trade Amount = 1 * 10 = 10 (buy $10 worth)

    -   Example of how to calculate Target Difference, Multiplier, and Trade
        Amount to sell:

            Target Difference = 20 - 30.24 = -10.24 (negative value is a sell signal)
            Multiplier = -10.24 / 10 ≈ -1.024 ≈ -1 (rounded to the nearest integer)
            Trade Amount = -1 * 10 = -10 (sell $10 worth)

12. Calculate the Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount
        Total Trade Amount = 10 + 0 = 10

13. Update Previous Total Trade Amount and Previous Total Order Size

        Previous Total Trade Amount = Total Trade Amount
        Previous Total Trade Amount = 10

        Previous Total Order Size = Total Order Size
        Previous Total Order Size = 0.00107124

### Calculating Record Entries

Now we can tabulate our Current Target, Current Value, Multiplier, Trade Amount,
Total Trade Amount, Principal Amount, Order Size, Total Order Size, and
Interval. This allows us to track the progress of our investment and gives us a
bird's-eye view of its performance over time.

Holding is usually enforced via a minimum or maximum trade amount and varies
amongst brokerages and is outside of the scope of this strategy.

**Note:** When implementing this strategy, be aware of the specific minimum and
maximum trade amounts enforced by the exchange you are using. These limits can
affect the execution of trades and should be taken into account when developing
your trading bot. Consider adding an environment variable or configuration
setting to handle these requirements, allowing you to easily adjust the values
based on the exchange's rules and restrictions.

| Datetime   | Market Price | Current Target | Current Value | Principal Amount | Multiplier | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| ---------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| 2020-01-01 | 9334.98      | 10.00          | 0.00          | 10.00            | 1.00       | 10.00        | 10.00              | 0.00107124 | 0.00107124       | 1        |
| 2020-02-01 | 8,505.07     | 20.00          |               |                  |            |              |                    |            |                  | 2        |

We can calculate the second record entry as follows:

1.  Define Principal Amount

        Principal Amount = Constant Float Value
        Principal Amount = 10.00

2.  Get the current datetime

        Datetime = Current Date
        Datetime = "2020-02-01"

3.  Get the current market price

        Market Price = Current Market Price
        Market Price = 8505.07

4.  Calculate the Interval

        Since there is a previous record:
        Interval = Previous Record Interval + 1
        Interval = 1 + 1 = 2

5.  Calculate the Current Target

        Current Target = Principal Amount * Interval
        Current Target = 10 * 2 = 20

6.  Get Previous Total Order Size

        Since there is a previous record:
        Previous Total Order Size = 0.00107124 (from the previous record)

7.  Calculate or get the Order Size

        Order Size = Principal Amount / Market Price
        Order Size = 10 / 8505.07 ≈ 0.00117577

8.  Calculate the Total Order Size

        Total Order Size = Order Size + Previous Total Order Size
        Total Order Size = 0.00117577 + 0.00107124 ≈ 0.00224701

9.  Calculate the Current Value

        Current Value = Market Price * Previous Total Order Size
        Current Value = 8505.07 * 0.00107124 ≈ 9.11

10. Calculate the Multiplier

    Determine how much should be bought or sold to get back to the Target Value.

        Target Difference = Current Target - Current Value
        Target Difference = 20 - 9.11 = 10.89

    Multiplier represents a value that is used to determine the size of the next
    trade.

        Multiplier = Target Difference / Principal Amount
        Multiplier = 10.89 / 10 = 1.089

    Enforce the Min Multiplier and Max Multiplier limits.

        IF Multiplier = 0
            THEN Multiplier = 1
        ELSE IF Multiplier > Max Multiplier
            THEN Multiplier = Max Multiplier
        ELSE IF Multiplier < -Max Multiplier
            THEN Multiplier = -Max Multiplier
        ELSE IF Multiplier < 0
            THEN Multiplier = -round(max(Min Multiplier, min(Multiplier, Max Multiplier)))
        ELSE
            Multiplier = round(max(Min Multiplier, min(Multiplier, Max Multiplier)))

    In this case, the Multiplier is within the limits:

        Multiplier = 1

11. Calculate the Trade Amount

        Trade Amount = Multiplier * Principal Amount
        Trade Amount = 1 * 10 = 10

12. Get or calculate Previous Total Trade Amount

        Since there is a previous record:
        Previous Total Trade Amount = 10 (from the previous record)

13. Calculate the Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount
        Total Trade Amount = 10 + 10 = 20

14. Update Previous Total Trade Amount and Previous Total Order Size

        Previous Total Trade Amount = Total Trade Amount
        Previous Total Trade Amount = 20

        Previous Total Order Size = Total Order Size
        Previous Total Order Size ≈ 0.00224701

The records will be created and updated sequentially as the bot executes each
order, following the steps outlined here.

| Datetime   | Market Price | Current Target | Current Value | Principal Amount | Multiplier | Trade Amount | Total Trade Amount | Order Size   | Total Order Size | Interval |
| ---------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ------------ | ------------------ | ------------ | ---------------- | -------- |
| 2020-01-01 | 9,334.98     | 10.00          | 0.00          | 10.00            | 1          | 10.00        | 10.00              | 0.00107124   | 0.00107124       | 1        |
| 2020-02-01 | 8,505.07     | 20.00          | 9.11          | 10.00            | 1          | 10.00        | 20.00              | 0.00117577   | 0.00224701       | 2        |
| 2020-03-01 | 6,424.35     | 30.00          | 14.43         | 10.00            | 2          | 20.00        | 40.00              | 0.00311315   | 0.00536017       | 3        |
| 2020-04-01 | 8,624.28     | 40.00          | 46.23         | 10.00            | -1         | (10.00)      | 30.00              | (0.00115952) | 0.00420065       | 4        |

## Summary

Dynamic Cost Averaging (DCA) is an investment strategy that aims to manage the
impact of market volatility by incrementally adjusting the investment amounts
based on a predefined set of rules. The strategy uses a constant principal
amount for each trade and adjusts the trade frequency and size based on market
conditions, enabling the investor to buy more when prices are low and sell when
prices are high. This can potentially lead to better long-term returns than
traditional Cost Averaging (CA).

Key components of the Dynamic Cost Averaging strategy:

1. Principal Amount: The constant amount used for each trade.
2. Interval: The frequency at which trades are executed (e.g., monthly).
3. Current Target: The cumulative target amount at the current interval
   (Principal Amount \* Interval).
4. Current Value: The total value of the asset based on the current market
   price.
5. Multiplier: A value used to determine the size of the next trade, calculated
   using the difference between the Current Target and Current Value.

The algorithm enforces limits on the minimum and maximum multipliers to prevent
over- or under-investment. To calculate the multiplier, the algorithm considers
the target difference, the principal amount, and the multiplier limits.

The main steps in the DCA algorithm are:

1. Define the Principal Amount and Interval.
2. Get the current Datetime and Market Price.
3. Calculate the Current Target, Current Value, and Multiplier.
4. Determine the Trade Amount, Total Trade Amount, Order Size, and Total Order
   Size.
5. Update the values and repeat the process for each Interval.

By using Dynamic Cost Averaging, investors can potentially mitigate the risks of
market fluctuations and achieve more consistent returns over time. The strategy
is adaptable to different market conditions, making it suitable for various
investment scenarios.

## Solution

    TODO

## Complete Data Set

    TODO

---

| Date       | Market Price | Current Target | Current Value | Principal Amount | Factor Purchase | Factor Amount | Total Factor Amount | Order Size | Total Order Size | Time Period |
| ---------- | ------------ | -------------- | ------------- | ---------------- | --------------- | ------------- | ------------------- | ---------- | ---------------- | ----------- |
| 2020-01-01 | 7174.33      | 100.00         | 0.00          | 100.00           | 1.00            | 100.00        | 100.00              | 0.01393858 | 0.01393858       | 1           |
| 2020-02-01 | 9380.18      | 200.00         | 130.75        | 100.00           | 1.00            | 100.00        | 200.00              | 0.01066078 | 0.02459936       | 2           |
| 2020-03-01 | 8522.31      | 300.00         | 209.64        | 100.00           | 1.00            | 100.00        | 300.00              | 0.01173391 | 0.03633327       | 3           |
| 2020-04-01 | 6666.11      | 400.00         | 242.20        | 100.00           | 2.00            | 200.00        | 500.00              | 0.01500125 | 0.05133452       | 4           |
| 2020-05-01 | 8829.42      | 500.00         | 453.25        | 100.00           | 1.00            | 100.00        | 600.00              | 0.01132577 | 0.06266029       | 5           |
| 2020-06-01 | 10208.96     | 600.00         | 639.70        | 100.00           | 1.00            | 100.00        | 700.00              | 0.00979532 | 0.07245561       | 6           |
| 2020-07-01 | 9239.97      | 700.00         | 669.49        | 100.00           | 1.00            | 100.00        | 800.00              | 0.01082255 | 0.08327816       | 7           |
| 2020-08-01 | 11810.07     | 800.00         | 983.52        | 100.00           | 1.00            | 100.00        | 900.00              | 0.00846735 | 0.09174551       | 8           |
| 2020-09-01 | 11924.22     | 900.00         | 1093.99       | 100.00           | 1.00            | 100.00        | 1000.00             | 0.00838629 | 0.10013180       | 9           |
| 2020-10-01 | 10617.63     | 1000.00        | 1063.16       | 100.00           | 1.00            | 100.00        | 1100.00             | 0.00941830 | 0.10955010       | 10          |
| 2020-11-01 | 13771.59     | 1100.00        | 1508.68       | 100.00           | 1.00            | 100.00        | 1200.00             | 0.00726133 | 0.11681142       | 11          |
| 2020-12-01 | 18782.97     | 1200.00        | 2194.07       | 100.00           | 1.00            | 100.00        | 1300.00             | 0.00532397 | 0.12213539       | 12          |

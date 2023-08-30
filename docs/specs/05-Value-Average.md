**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research.**_

# Value Averaging

Value Averaging is similar to Cost Averaging. We set a Principal Amount and then
purchase an asset with the Principal Amount based on a set Interval and Growth
Rate.

We need to define our columns: Datetime, Market Price, Current Target, Current
Value, Trade Amount, Total Trade Amount, Order Size, Total Order Size, and
Interval. This will allow us to keep track of the relevant data and show the
evaluated expressions as its set of results.

## Algorithm

1.  **Define Principal Amount**

        Principal Amount = Constant Float Value

2.  **Define Annual Interest Rate**

        Annual Interest Rate = Constant Float Value

3.  **Define Frequency**

        Frequency = One of 365 (Daily), 52 (Weekly), 12 (Monthly)

4.  **Define Time Period**

        Time Period = 1 / Frequency  # Time in years for one interval

5.  **Get Datetime**

        Datetime = Current Datetime

6.  **Get Market Price**

        Market Price = Current Market Price

7.  **Get Interval**

        IF no previous records
            THEN Interval = 1
        Increment Interval with each record insertion
            Interval = Previous Interval + 1

8.  **Get Current Target**

        IF no previous records
            THEN Current Target = Principal Amount
        IF Previous Current Target
            THEN Current Target = Principal Amount * Interval * (1 + (Annual Interest Rate / Frequency))^Interval

9.  **Get Previous Total Order Size**

        IF no previous records
            THEN set Previous Total Order Size to 0
        OTHERWISE, set Previous Total Order Size to sum of Order Size column, excluding current record
            Previous Total Order Size = sum(Order Size) for all previous records

10. **Get Order Size**

        Order Size = Trade Amount / Market Price

11. **Get Total Order Size**

        Total Order Size = Order Size + Previous Total Order Size

12. **Get Current Value**

        Current Value = Market Price * Previous Total Order Size

13. **Get Previous Total Trade Amount**

        IF no previous records
                THEN Previous Total Trade Amount = 0
        OTHERWISE, Previous Total Trade Amount is sum of Trade Amount column excluding current record
                Previous Total Trade Amount = sum(Trade Amount) for all previous records

14. **Get Trade Amount**

        Trade Amount = Current Target - Current Value

        IF Trade Amount > 0
            THEN buy Trade Amount
        IF Trade Amount < 0
            THEN sell Trade Amount

        NOTE: Buying and Selling should be determined by a `MIN_TRADE_AMOUNT` to avoid erroneous record entries.

15. **Get Total Trade Amount**

        Total Trade Amount = Trade Amount + Previous Total Trade Amount

## Walkthrough

I want to paper trade a Value Averaging strategy, investing $10 per month in the
BTC-USD trading pair over a 1-year period. I will make the investments on the
first day of each month in 2020.

The smallest units for US dollars are denominated in "cents" and will use a
precision of:

        1 * 10 ^ -2 = 0.01

The smallest units for Bitcoin are denominated in "satoshis" and will use a
precision of:

        1 * 10 ^ -8 = 0.00000001

### Creating the Initial Record

Let's initialize the table and calculate the first record: Initialize the table
and calculate the first record:

1.  Set Interval, Previous Total Order Size, and Previous Total Trade Amount

        Interval = 1
        Previous Total Order Size = 0
        Previous Total Trade Amount = 0

2.  Set Principal Amount

        Principal Amount = 10.00

3.  Set the Interest Rate and Frequency. We set the Interest Rate to 10% and the
    Frequency to 12 (Monthly). Then, calculate the Growth Rate.

        Interest Rate = 0.10
        Frequency = 12
        Growth Rate = 1 + (Interest Rate / Frequency) = 1 + (0.10 / 12) ≈ 1.008333

4.  Get Datetime

        Datetime = "2020-01-01"

5.  Get Market Price

        Market Price = 9334.98

6.  Get Current Target. For the first record, Current Target is set equal to the
    Principal Amount, reflecting the initial investment. In subsequent records,
    Current Target is calculated using
    `Principal Amount * Interval * pow(1 + (Annual Interest Rate / Frequency), Interval)`
    to achieve the specified growth rate over time.

        Current Target = 10.00

7.  Get Order Size

        Order Size = 10.00 / 9334.98 ≅ 0.001071319809734191 ≅ 0.00107132

8.  Get Total Order Size

        Total Order Size = 0.00107132 + 0 = 0.00107132

9.  Get Current Value

        Current Value = 9334.98 * 0 = 0

10. Get Trade Amount

        Trade Amount = 10.00 - 0 = 10.00

11. Get Total Trade Amount

        Total Trade Amount = 10.00 + 0 = 10.00

12. Update Previous Total Order Size and Previous Total Trade Amount

        Previous Total Order Size = 0.00107132
        Previous Total Trade Amount = 10.00

### Calculating Record Entries

Now we can tabulate our Current Target, Current Value, Trade Amount, Total Trade
Amount, Order Size, and Total Order Size.

This allows us to track our investment over time and signals whether we should
buy, sell, or hold.

Holding is usually enforced via a minimum or maximum trade amount and varies
amongst brokerages and is outside of the scope of this strategy.

**Note:** When implementing this strategy, be aware of the specific minimum and
maximum trade amounts enforced by the exchange you are using. These limits can
affect the execution of trades and should be taken into account when developing
your trading bot. Consider adding an environment variable or configuration
setting to handle these requirements, allowing you to easily adjust the values
based on the exchange's rules and restrictions.

| Exchange | Date     | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| paper    | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 10.00        | 10.00              | 0.00107124 | 0.00107124       | 1        |
| paper    | 02/01/20 | 8,505.07     |                |               |              |                    |            |                  | 2        |

1.  Get Datetime

        Datetime = "2020-02-01"

2.  Get Market Price

        Market Price = 8505.07

3.  Get Interval

        Interval = 1 + 1 = 2

4.  Get Current Target

        Current Target = 10.00 * 2 * pow(1.008333, 2) ≅ 20.334708777779994 ≅ 20.33

5.  Get Current Value

        Current Value = 8505.07 * 0.00107124 ≅ 9.1109711868 ≅ 9.11

6.  Get Trade Amount

        Trade Amount = 20.33 - 9.11 = 11.22

7.  Get Total Trade Amount

        Total Trade Amount = 11.22 + 10.00 = 21.22

8.  Get Order Size

        Order Size = 11.22 / 8505.07 ≅ 0.0013192131281694333 ≅ 0.00131965

9.  Get Total Order Size

        Total Order Size = 0.00131965 + 0.00107124 = 0.00239089

10. Update Previous Total Order Size and Previous Total Trade Amount

        Previous Total Order Size = 0.00239089
        Previous Total Trade Amount = 21.22

11. Repeat steps 1 through 10 until each record has been evaluated

The records will be created and updated sequentially as the bot executes each
order, following the steps outlined here.

| Exchange | Date     | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| paper    | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 10.00        | 10.00              | 0.00107124 | 0.00107124       | 1        |
| paper    | 02/01/20 | 8,505.07     | 20.33          | 9.11          | 11.22        | 21.22              | 0.00131965 | 0.00239089       | 2        |
| paper    | 03/01/20 | 6,424.35     | 30.76          |               |              |                    |            |                  | 3        |
| paper    | 04/01/20 | 8,624.28     |                |               |              |                    |            |                  | 4        |
| paper    | 05/01/20 | 9,446.57     |                |               |              |                    |            |                  | 5        |

Try completing the table as an exercise.

## Summary

Value Averaging is an investment strategy that aims to maintain a consistent
growth rate for an investment over time. It takes into account the principal
amount, growth rate, and interval, adjusting trades accordingly to achieve the
desired value at each interval. By buying more when the market price is lower
and selling when the market price is higher, it seeks to maintain a consistent
growth trajectory.

The steps to implement the Value Averaging strategy are:

1. Define initial parameters (Principal Amount, Growth Rate, and Interval).
2. Calculate the Current Target using the formula
   `Principal Amount * Interval * pow(Growth Rate, Interval)`.
3. Evaluate the Current Value of the investment.
4. Determine the Trade Amount by finding the difference between the Current
   Target and the Current Value.
5. Calculate the Order Size by dividing the Trade Amount by the Market Price.
6. Update the Total Order Size and Total Trade Amount based on the calculated
   Order Size and Trade Amount.
7. Keep track of the Current Target, Current Value, Trade Amount, Total Trade
   Amount, Order Size, and Total Order Size for each interval.
8. Be aware of the specific minimum and maximum trade amounts enforced by the
   exchange you are using, and consider adding an environment variable or
   configuration setting to handle these requirements.

By following these steps and adjusting trades based on market fluctuations, the
Value Averaging strategy aims to achieve consistent growth and reduce the impact
of market volatility on an investment portfolio.

## Solution

| Exchange | Date     | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size  | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ----------- | ---------------- | -------- |
| paper    | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 10.00        | 10.00              | 0.00107124  | 0.00107124       | 1        |
| paper    | 02/01/20 | 8,505.07     | 20.33          | 9.11          | 11.22        | 21.22              | 0.00131965  | 0.00239089       | 2        |
| paper    | 03/01/20 | 6,424.35     | 30.76          | 15.36         | 15.40        | 36.62              | 0.00239655  | 0.00478745       | 3        |
| paper    | 04/01/20 | 8,624.28     | 41.35          | 41.29         | 0.06         | 36.68              | 0.00000716  | 0.00479461       | 4        |
| paper    | 05/01/20 | 9,446.57     | 52.12          | 45.29         | 6.83         | 43.51              | 0.00072255  | 0.00551716       | 5        |
| paper    | 06/01/20 | 9,136.20     | 63.06          | 50.41         | 12.66        | 56.16              | 0.00138539  | 0.00690255       | 6        |
| paper    | 07/01/20 | 11,351.62    | 74.19          | 78.36         | (4.17)       | 52.00              | -0.00036721 | 0.00653534       | 7        |
| paper    | 08/01/20 | 11,655.00    | 85.49          | 76.17         | 9.32         | 61.32              | 0.00079982  | 0.00733516       | 8        |
| paper    | 09/01/20 | 10,779.63    | 96.98          | 79.07         | 17.91        | 79.23              | 0.00166136  | 0.00899652       | 9        |
| paper    | 10/01/20 | 13,804.81    | 108.65         | 124.20        | (15.54)      | 63.68              | -0.00112589 | 0.00787063       | 10       |
| paper    | 11/01/20 | 19,713.94    | 120.51         | 155.16        | (34.65)      | 29.04              | -0.00175751 | 0.00611312       | 11       |
| paper    | 12/01/20 | 28,990.08    | 132.57         | 177.22        | (44.65)      | (15.62)            | -0.00154035 | 0.00457277       | 12       |

## Complete Data Set

| Exchange | Date     | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size  | Total Order Size | Interval |
| -------- | -------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ----------- | ---------------- | -------- |
| paper    | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 10.00        | 10.00              | 0.00107124  | 0.00107124       | 1        |
| paper    | 02/01/20 | 8,505.07     | 20.33          | 9.11          | 11.22        | 21.22              | 0.00131965  | 0.00239089       | 2        |
| paper    | 03/01/20 | 6,424.35     | 30.76          | 15.36         | 15.40        | 36.62              | 0.00239655  | 0.00478745       | 3        |
| paper    | 04/01/20 | 8,624.28     | 41.35          | 41.29         | 0.06         | 36.68              | 0.00000716  | 0.00479461       | 4        |
| paper    | 05/01/20 | 9,446.57     | 52.12          | 45.29         | 6.83         | 43.51              | 0.00072255  | 0.00551716       | 5        |
| paper    | 06/01/20 | 9,136.20     | 63.06          | 50.41         | 12.66        | 56.16              | 0.00138539  | 0.00690255       | 6        |
| paper    | 07/01/20 | 11,351.62    | 74.19          | 78.36         | (4.17)       | 52.00              | -0.00036721 | 0.00653534       | 7        |
| paper    | 08/01/20 | 11,655.00    | 85.49          | 76.17         | 9.32         | 61.32              | 0.00079982  | 0.00733516       | 8        |
| paper    | 09/01/20 | 10,779.63    | 96.98          | 79.07         | 17.91        | 79.23              | 0.00166136  | 0.00899652       | 9        |
| paper    | 10/01/20 | 13,804.81    | 108.65         | 124.20        | (15.54)      | 63.68              | -0.00112589 | 0.00787063       | 10       |
| paper    | 11/01/20 | 19,713.94    | 120.51         | 155.16        | (34.65)      | 29.04              | -0.00175751 | 0.00611312       | 11       |
| paper    | 12/01/20 | 28,990.08    | 132.57         | 177.22        | (44.65)      | (15.62)            | -0.00154035 | 0.00457277       | 12       |
| paper    | 01/01/21 | 33,137.74    | 144.81         | 151.53        | (6.72)       | (22.34)            | -0.00020287 | 0.00436991       | 13       |
| paper    | 02/01/21 | 45,231.75    | 157.25         | 197.66        | (40.41)      | (62.75)            | -0.00089342 | 0.00347649       | 14       |
| paper    | 03/01/21 | 58,800.00    | 169.88         | 204.42        | (34.53)      | (97.29)            | -0.00058731 | 0.00288917       | 15       |
| paper    | 04/01/21 | 57,798.77    | 182.72         | 166.99        | 15.73        | (81.56)            | 0.00027212  | 0.00316130       | 16       |
| paper    | 05/01/21 | 37,279.31    | 195.76         | 117.85        | 77.91        | (3.65)             | 0.00208979  | 0.00525108       | 17       |
| paper    | 06/01/21 | 35,060.00    | 209.00         | 184.10        | 24.90        | 21.24              | 0.00071010  | 0.00596118       | 18       |
| paper    | 07/01/21 | 41,495.01    | 222.45         | 247.36        | (24.91)      | (3.67)             | -0.00060033 | 0.00536085       | 19       |
| paper    | 08/01/21 | 47,112.50    | 236.11         | 252.56        | (16.46)      | (20.12)            | -0.00034928 | 0.00501157       | 20       |
| paper    | 09/01/21 | 43,824.43    | 249.98         | 219.63        | 30.35        | 10.23              | 0.00069253  | 0.00570409       | 21       |
| paper    | 10/01/21 | 61,343.68    | 264.06         | 349.91        | (85.85)      | (75.62)            | -0.00139942 | 0.00430468       | 22       |
| paper    | 11/01/21 | 56,987.97    | 278.37         | 245.31        | 33.05        | (42.56)            | 0.00058001  | 0.00488468       | 23       |
| paper    | 12/01/21 | 46,211.24    | 292.89         | 225.73        | 67.16        | 24.60              | 0.00145342  | 0.00633810       | 24       |
| paper    | 01/01/22 | 38,491.93    | 307.64         | 243.97        | 63.67        | 88.27              | 0.00165416  | 0.00799226       | 25       |
| paper    | 02/01/22 | 43,192.66    | 322.61         | 345.21        | (22.60)      | 65.67              | -0.00052319 | 0.00746908       | 26       |
| paper    | 03/01/22 | 45,528.45    | 337.81         | 340.06        | (2.25)       | 63.43              | -0.00004934 | 0.00741973       | 27       |
| paper    | 04/01/22 | 37,644.10    | 353.24         | 279.31        | 73.93        | 137.36             | 0.00196393  | 0.00938367       | 28       |
| paper    | 05/01/22 | 31,784.05    | 368.90         | 298.25        | 70.65        | 208.01             | 0.00222291  | 0.01160658       | 29       |
| paper    | 06/01/22 | 19,985.62    | 384.80         | 231.96        | 152.84       | 360.85             | 0.00764751  | 0.01925409       | 30       |
| paper    | 07/01/22 | 23,307.44    | 400.95         | 448.76        | (47.82)      | 313.03             | -0.00205163 | 0.01720246       | 31       |
| paper    | 08/01/22 | 20,048.26    | 417.33         | 344.88        | 72.45        | 385.48             | 0.00361370  | 0.02081616       | 32       |
| paper    | 09/01/22 | 19,426.11    | 433.96         | 404.38        | 29.58        | 415.06             | 0.00152262  | 0.02233878       | 33       |
| paper    | 10/01/22 | 20,489.94    | 450.83         | 457.72        | (6.89)       | 408.17             | -0.00033620 | 0.02200258       | 34       |
| paper    | 11/01/22 | 17,167.33    | 467.96         | 377.73        | 90.23        | 498.40             | 0.00525609  | 0.02725867       | 35       |
| paper    | 12/01/22 | 16,530.35    | 485.34         | 450.60        | 34.74        | 533.15             | 0.00210185  | 0.02936052       | 36       |

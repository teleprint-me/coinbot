**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research**._

# Cost Averaging

Cost Averaging is an investment strategy that involves setting a fixed Principal
Amount and periodically purchasing an asset at that amount based on a
predetermined Frequency. This approach aims to spread investment over time,
reducing the impact of market fluctuations.

The columns for our data table are: Datetime, Market Price, Current Target,
Current Value, Order Size, Total Order Size, and Interval. This structure keeps
the tabulation of our data simple and compact.

## Overview

1.  Define Principal Amount

        Principal Amount = Constant Float Value

2.  Define Frequency

        Frequency = One of 365 (Daily), 52 (Weekly), 12 (Monthly)

3.  Get Datetime

        Datetime = Current Datetime

4.  Get Market Price

        Market Price = Current Market Price

5.  Get Interval

        IF no previous records
            THEN Interval = 1
        Increment Interval with each record insertion
            Interval = Previous Interval + 1

6.  Get Current Target

        IF no previous records
            THEN Current Target = Principal Amount
        IF Previous Current Target
            THEN Current Target = Principal Amount + Previous Current Target

7.  Get Previous Total Order Size

        IF no previous records
            THEN set Previous Total Order Size to 0
        OTHERWISE, set Previous Total Order Size to sum of Order Size column, excluding current record
            Previous Total Order Size = sum(Order Size) for all previous records

8.  Get Order Size

        Order Size = Trade Amount / Market Price

9.  Get Total Order Size

        Total Order Size = Order Size + Previous Total Order Size

10. Get Current Value

        Current Value = Market Price * Previous Total Order Size

## Understanding Cost Averaging

### Variables

Each variable represents the following:

-   **Interval**: The number of time units that have passed since the start of
    the investment strategy. The interval is a variable that changes over time.
-   **Principal Amount**: The fixed amount of money invested at each interval.
    In this example, the principal amount is set to $10.00.
-   **Frequency**: The frequency at which the asset is purchased. It can be set
    to "daily", "weekly", or "monthly". In this example, the frequency is set to
    "monthly".
    -   **Daily**: Indicates an investment made every day, resulting in 365
        investments per year.
    -   **Weekly**: Indicates an investment made once a week, resulting in 52
        investments per year.
    -   **Monthly**: Indicates an investment made once a month, resulting in 12
        investments per year.

These variables help to define and execute a cost averaging investment strategy
tailored to the investor's preferences and risk tolerance.

### Defining Paper Trading Parameters

In this example, we will Paper Trade $10 per month on a yearly basis using the
BTC-USD trade pair over a 1-year period in 2020.

### Calculating Record Entries

We need to define how each record is calculated by filling out each cell with
the appropriate data.

1.  Calculate Interval

        If there is no previous Interval, then set Interval to 1
        Otherwise increment Interval on inserted record
            Interval = Interval + 1

2.  Calculate Current Target

        current_target = principal_amount * interval

3.  Calculate Order Size

        order_size = principal_amount / market_price

4.  Calculate Previous Total Order Size

        If there is no Previous Total Order Size
        then set Previous Total Order Size to 0.
            previous_total_order_size = 0
        Otherwise Previous Total Order Size represents sum of Order Size
        column excluding Current Record.
            previous_total_order_size = sum(order_size_column[:-1])

5.  Calculate Total Order Size

        total_order_size = order_size + previous_total_order_size

6.  Calculate Current Value

        current_value = market_price * previous_total_order_size

Each variable represents the following:

-   **interval**: The number of time units that have passed since the start of
    the investment strategy. The interval is incremented for each record entry.
-   **current_target**: The target investment amount at the current interval,
    calculated as the `principal_amount` multiplied by the `interval`.
-   **order_size**: The amount of the asset to be purchased at the current
    market price, calculated as the principal amount divided by the price.
-   **previous_total_order_size**: The sum of the Order Size column excluding
    the current record. If no previous total order size exists, set it to `0`.
-   **total_order_size**: The sum of the current order size and the previous
    total order size.
-   **current_value**: The value of the investment at the current market price,
    calculated as the market price multiplied by the previous total order size.

This method of calculation helps track the progress of the paper trading
investment strategy and provides insights into its performance over time.

### Initializing Variables and Tabulating Data

Let's start by initializing both `previous_total_order_size` and `interval`:

-   `previous_total_order_size: float = 0`
-   `interval: int = 1`

Now we can tabulate our Current Target, Current Value, Order Size, Total Order
Size, and Interval. This allows us to track the progress of our investment and
gives us a bird's-eye view of its performance over time.

### Handling the Current Value Calculation

It's important to note that the Current Value calculation depends on whether or
not it includes the current record's Total Order Size:

    If the record is the Initial Record, then the `current_value` is
    initialized to zero: `current_value: float = 0`, because there is no
    investment yet.

    If there is at least one record, then the `current_value` calculation uses
    `previous_total_order_size`:
        current_value: float = market_price * previous_total_order_size

| Date     | Market Price | Current Target | Current Value | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | ---------- | ---------------- | -------- |
| 01/01/20 | 9,334.98     | 10.00          | 0.00          | 0.00107124 | 0.00107124       | 1        |
| 02/01/20 | 8,505.07     | 20.00          | 9.11          | 0.00117577 | 0.00224701       | 2        |
| 03/01/20 | 6,424.35     | 30.00          | 14.44         | 0.00155658 | 0.00380359       | 3        |
| 04/01/20 | 8,624.28     | 40.00          | 32.80         | 0.00115952 | 0.00496310       | 4        |
| 05/01/20 | 9,446.57     | 50.00          | 46.88         | 0.00105859 | 0.00602169       | 5        |
| 06/01/20 | 9,136.20     | 60.00          | 55.02         |            |                  | 6        |
| 07/01/20 | 11,351.62    | 70.00          |               |            |                  | 7        |
| 08/01/20 | 11,655.00    | 80.00          |               |            |                  | 8        |
| 09/01/20 | 10,779.63    | 90.00          |               |            |                  | 9        |
| 10/01/20 | 13,804.81    | 100.00         |               |            |                  | 10       |
| 11/01/20 | 19,713.94    |                |               |            |                  | 11       |
| 12/01/20 | 28,990.08    |                |               |            |                  | 12       |

Try completing the table as an exercise. It's already more than halfway there
for you.

## Tracking Investment Performance with Gain or Loss

In this example, we'll add a Gain or (Loss) column to provide more information
about our investment performance at a glance.

| Date     | Market Price | Current Target | Current Value | Gain or (Loss) | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | -------------- | ---------- | ---------------- | -------- |
| 01/01/20 | 9,334.98     | 10.00          | 0.00          | 0.00           | 0.00107124 | 0.00107124       | 1        |
| 02/01/20 | 8,505.07     | 20.00          | 9.11          | (0.89)         | 0.00117577 | 0.00224701       | 2        |
| 03/01/20 | 6,424.35     | 30.00          | 14.44         | (5.56)         | 0.00155658 | 0.00380359       | 3        |
| 04/01/20 | 8,624.28     | 40.00          | 32.80         | 2.80           | 0.00115952 | 0.00496310       | 4        |
| 05/01/20 | 9,446.57     | 50.00          | 46.88         | 6.88           | 0.00105859 | 0.00602169       | 5        |

The Gain or (Loss) column represents the difference between the `current_value`
and the `previous_current_target`. It can be calculated using the formula:

    gain_or_loss = current_value - previous_current_target

A positive value represents a gain, while a negative value represents a loss.

The table shows that the investment remains in an unrealized loss until the 4th
record entry. The investment becomes realized once it is sold.

The table also demonstrates how the `order_size` is affected by the
`market_price`. We buy less when the price is high and buy more when the price
is low. This trend becomes more apparent as the price increases or decreases.

As an exercise, try completing the table to further understand the investment
performance.

## Models

### Base Model

```python
@dataclass
class AverageRecord:
    """A dataclass representing a base record for averaging strategies."""

    exchange: str
    product_id: str
    principal_amount: float
    side: str
    datetime: str
    market_price: float
    current_target: float
    current_value: float
    order_size: float
    total_order_size: float
    interval: int = 0

    @property
    def base(self) -> str:
        return self.product_id.split("-")[0]

    @property
    def quote(self) -> str:
        return self.product_id.split("-")[1]
```

The `AverageRecord` dataclass serves as the base model for averaging strategies.
It contains attributes such as exchange, product_id, datetime, principal_amount,
market_price, side, current_target, current_value, order_size, total_order_size,
and interval. The class also includes two properties: `base` and `quote`,
derived from the product_id, and a method called `increment_interval` to
increment the interval attribute.

### Cost Average Model

```python
@dataclass
class CostAverageRecord(AverageRecord):
    gain_loss: float = 0
```

The `CostAverageRecord` dataclass extends the `AverageRecord` and adds an
optional `gain_loss` attribute, which represents the gain or loss in the
averaging strategy.

## Pseudocode

1. Read environment variables

    a. Get the EXCHANGE, PRODUCT_ID, PRINCIPAL_AMOUNT.

2. Create a broker instance using the `broker_factory` function with the
   EXCHANGE.

3. Read the existing records from the CSV file or create a new file if it
   doesn't exist, using `read_write_csv` from the `io` module.

4. If the existing records have at least one data row (excluding the header),
   convert the CSV dataset from a `list[list[str]]` to a
   `list[CostAverageRecord]`. Otherwise, initialize an empty list for storing
   `CostAverageRecord` objects.

5. If the list of records is not empty:

    a. Get the last record from the list and extract any necessary values.

6. Execute or simulate an order using the broker:

    a. If execute flag is True, call the broker's `order` method with the
    PRINCIPAL_AMOUNT and PRODUCT_ID.

    b. If execute flag is False, simulate the order without actually placing it.

7. Retrieve the order information, including datetime, market_price, side, and
   quote_size.

8. Calculate the current target, current value, total order size, and gain or
   loss if applicable.

9. Create a `CostAverageRecord` object with the extracted and calculated values,
   and the incremented interval.

10. Append the new `CostAverageRecord` object to the list of records.

11. Convert the list of `CostAverageRecord` objects back to a `list[list[str]]`.

12. Print the updated records using `print_csv` from the `io` module.

13. Write the updated records to the CSV file using `write_csv` from the `io`
    module.

14. Exit the program.

## Summary

Summary goes here.

## Solution

| Exchange | Principal Amount | Date     | Market Price | Current Target | Current Value | Gain or (Loss) | Order Size | Total Order Size | Interval |
| -------- | ---------------- | -------- | ------------ | -------------- | ------------- | -------------- | ---------- | ---------------- | -------- |
| paper    | 10.00            | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 0.00           | 0.00107124 | 0.00107124       | 1        |
| paper    | 10.00            | 02/01/20 | 8,505.07     | 20.00          | 9.11          | (0.89)         | 0.00117577 | 0.00224701       | 2        |
| paper    | 10.00            | 03/01/20 | 6,424.35     | 30.00          | 14.44         | (5.56)         | 0.00155658 | 0.00380359       | 3        |
| paper    | 10.00            | 04/01/20 | 8,624.28     | 40.00          | 32.80         | 2.80           | 0.00115952 | 0.00496310       | 4        |
| paper    | 10.00            | 05/01/20 | 9,446.57     | 50.00          | 46.88         | 6.88           | 0.00105859 | 0.00602169       | 5        |
| paper    | 10.00            | 06/01/20 | 9,136.20     | 60.00          | 55.02         | 5.02           | 0.00109455 | 0.00711624       | 6        |
| paper    | 10.00            | 07/01/20 | 11,351.62    | 70.00          | 80.78         | 20.78          | 0.00088093 | 0.00799717       | 7        |
| paper    | 10.00            | 08/01/20 | 11,655.00    | 80.00          | 93.21         | 23.21          | 0.00085800 | 0.00885517       | 8        |
| paper    | 10.00            | 09/01/20 | 10,779.63    | 90.00          | 95.46         | 15.46          | 0.00092768 | 0.00978284       | 9        |
| paper    | 10.00            | 10/01/20 | 13,804.81    | 100.00         | 135.05        | 45.05          | 0.00072439 | 0.01050723       | 10       |
| paper    | 10.00            | 11/01/20 | 19,713.94    | 110.00         | 207.14        | 107.14         | 0.00050726 | 0.01101448       | 11       |
| paper    | 10.00            | 12/01/20 | 28,990.08    | 120.00         | 319.31        | 209.31         | 0.00034495 | 0.01135943       | 12       |

## Complete Data Set

| Exchange | Principal Amount | Date     | Market Price | Current Target | Current Value | Gain or (Loss) | Order Size | Total Order Size | Interval |
| -------- | ---------------- | -------- | ------------ | -------------- | ------------- | -------------- | ---------- | ---------------- | -------- |
| paper    | 10.00            | 01/01/20 | 9,334.98     | 10.00          | 0.00          | 0.00           | 0.00107124 | 0.00107124       | 1        |
| paper    | 10.00            | 02/01/20 | 8,505.07     | 20.00          | 9.11          | (0.89)         | 0.00117577 | 0.00224701       | 2        |
| paper    | 10.00            | 03/01/20 | 6,424.35     | 30.00          | 14.44         | (5.56)         | 0.00155658 | 0.00380359       | 3        |
| paper    | 10.00            | 04/01/20 | 8,624.28     | 40.00          | 32.80         | 2.80           | 0.00115952 | 0.00496310       | 4        |
| paper    | 10.00            | 05/01/20 | 9,446.57     | 50.00          | 46.88         | 6.88           | 0.00105859 | 0.00602169       | 5        |
| paper    | 10.00            | 06/01/20 | 9,136.20     | 60.00          | 55.02         | 5.02           | 0.00109455 | 0.00711624       | 6        |
| paper    | 10.00            | 07/01/20 | 11,351.62    | 70.00          | 80.78         | 20.78          | 0.00088093 | 0.00799717       | 7        |
| paper    | 10.00            | 08/01/20 | 11,655.00    | 80.00          | 93.21         | 23.21          | 0.00085800 | 0.00885517       | 8        |
| paper    | 10.00            | 09/01/20 | 10,779.63    | 90.00          | 95.46         | 15.46          | 0.00092768 | 0.00978284       | 9        |
| paper    | 10.00            | 10/01/20 | 13,804.81    | 100.00         | 135.05        | 45.05          | 0.00072439 | 0.01050723       | 10       |
| paper    | 10.00            | 11/01/20 | 19,713.94    | 110.00         | 207.14        | 107.14         | 0.00050726 | 0.01101448       | 11       |
| paper    | 10.00            | 12/01/20 | 28,990.08    | 120.00         | 319.31        | 209.31         | 0.00034495 | 0.01135943       | 12       |
| paper    | 10.00            | 01/01/21 | 33,137.74    | 130.00         | 376.43        | 256.43         | 0.00030177 | 0.01166120       | 13       |
| paper    | 10.00            | 02/01/21 | 45,231.75    | 140.00         | 527.46        | 397.46         | 0.00022108 | 0.01188228       | 14       |
| paper    | 10.00            | 03/01/21 | 58,800.00    | 150.00         | 698.68        | 558.68         | 0.00017007 | 0.01205235       | 15       |
| paper    | 10.00            | 04/01/21 | 57,798.77    | 160.00         | 696.61        | 546.61         | 0.00017301 | 0.01222537       | 16       |
| paper    | 10.00            | 05/01/21 | 37,279.31    | 170.00         | 455.75        | 295.75         | 0.00026825 | 0.01249361       | 17       |
| paper    | 10.00            | 06/01/21 | 35,060.00    | 180.00         | 438.03        | 268.03         | 0.00028523 | 0.01277884       | 18       |
| paper    | 10.00            | 07/01/21 | 41,495.01    | 190.00         | 530.26        | 350.26         | 0.00024099 | 0.01301983       | 19       |
| paper    | 10.00            | 08/01/21 | 47,112.50    | 200.00         | 613.40        | 423.40         | 0.00021226 | 0.01323209       | 20       |
| paper    | 10.00            | 09/01/21 | 43,824.43    | 210.00         | 579.89        | 379.89         | 0.00022818 | 0.01346027       | 21       |
| paper    | 10.00            | 10/01/21 | 61,343.68    | 220.00         | 825.70        | 615.70         | 0.00016302 | 0.01362329       | 22       |
| paper    | 10.00            | 11/01/21 | 56,987.97    | 230.00         | 776.36        | 556.36         | 0.00017548 | 0.01379876       | 23       |
| paper    | 10.00            | 12/01/21 | 46,211.24    | 240.00         | 637.66        | 407.66         | 0.00021640 | 0.01401516       | 24       |
| paper    | 10.00            | 01/01/22 | 38,491.93    | 250.00         | 539.47        | 299.47         | 0.00025979 | 0.01427495       | 25       |
| paper    | 10.00            | 02/01/22 | 43,192.66    | 260.00         | 616.57        | 366.57         | 0.00023152 | 0.01450648       | 26       |
| paper    | 10.00            | 03/01/22 | 45,528.45    | 270.00         | 660.46        | 400.46         | 0.00021964 | 0.01472612       | 27       |
| paper    | 10.00            | 04/01/22 | 37,644.10    | 280.00         | 554.35        | 284.35         | 0.00026565 | 0.01499176       | 28       |
| paper    | 10.00            | 05/01/22 | 31,784.05    | 290.00         | 476.50        | 196.50         | 0.00031462 | 0.01530639       | 29       |
| paper    | 10.00            | 06/01/22 | 19,985.62    | 300.00         | 305.91        | 15.91          | 0.00050036 | 0.01580675       | 30       |
| paper    | 10.00            | 07/01/22 | 23,307.44    | 310.00         | 368.41        | 68.41          | 0.00042905 | 0.01623580       | 31       |
| paper    | 10.00            | 08/01/22 | 20,048.26    | 320.00         | 325.50        | 15.50          | 0.00049880 | 0.01673459       | 32       |
| paper    | 10.00            | 09/01/22 | 19,426.11    | 330.00         | 325.09        | 5.09           | 0.00051477 | 0.01724936       | 33       |
| paper    | 10.00            | 10/01/22 | 20,489.94    | 340.00         | 353.44        | 23.44          | 0.00048804 | 0.01773741       | 34       |
| paper    | 10.00            | 11/01/22 | 17,167.33    | 350.00         | 304.50        | (35.50)        | 0.00058250 | 0.01831991       | 35       |
| paper    | 10.00            | 12/01/22 | 16,530.35    | 360.00         | 302.83        | (47.17)        | 0.00060495 | 0.01892486       | 36       |

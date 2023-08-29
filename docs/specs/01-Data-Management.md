**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research**._

# Data Management

Data is typically tracked alongside the execution of investment strategies. The
tracked data creates a data set, which is a collection of data.
[[3]](https://en.wikipedia.org/wiki/Data_set) This data is then
[tabulated](https://www.merriam-webster.com/dictionary/tabulate), resulting in a
data table. [[4]](https://en.wikipedia.org/wiki/Table_(database)) The tabulated
data consists of columns where every column of a table represents a variable,
and each row corresponds to a given record of the data set.

A table cell is one grouping within a table used for storing information or
data. Cells are grouped horizontally (rows of cells) and vertically (columns of
cells). Each cell contains information relating to the combination of the row
and column headings it is
[collinear](https://www.merriam-webster.com/dictionary/collinear) with.
[[5]](https://en.wikipedia.org/wiki/Table_cell) A series of simple mathematical
formulas can determine the value that resides within each cell. Each cell may be
the result of a constant or variable.

## Tabulating data sets

A table may contain any set of columns relevant to the data set, causing each
table to vary in its utilization by different investors. The table columns are
typically chosen to reflect the information the investor is interested in.

We will set up our own custom table and build upon it, starting with Cost
Averaging, then moving onto Dynamic Cost Averaging, and finally Value Averaging.

Our initial table will be kept as simple as possible, and we will add to it once
we've completed covering [First Principles](https://fs.blog/first-principles/).

We'll use Bitcoin's 2020 _closing prices_ as our sample data set. This will
allow us to _paper trade_ with the data set provided from 2020. The volatility
in Bitcoin will help showcase how each strategy performs. Bitcoin will be our
_base currency_, and the Dollar will be our _quote currency_. The base and quote
product create the _trade pair_ "_BTC-USD_".

A **trade pair** refers to the two currencies being traded against each other in
a currency exchange. In this case, BTC-USD represents a trade in which Bitcoin
(BTC) is traded for United States Dollars (USD).

The **base currency** is the first currency listed in a _currency pair_ and
represents the currency being bought or sold. In the BTC-USD trade pair, BTC is
the base currency, and you are either buying or selling Bitcoin.

The **quote currency** is the second currency listed in a _currency pair_ and
represents the currency used to buy or sell the base currency. In the BTC-USD
trade pair, USD is the quote currency, and you are buying or selling Bitcoin
with US dollars.

## Gathering Data Sets

The following data set represents the _closing prices_ for Bitcoin on the _first
day of each month_ in the year 2020.

| Month | Day | Year | Closing Price |
| ----- | --- | ---- | ------------- |
| Jan   | 01  | 2020 | $9334.98      |
| Feb   | 01  | 2020 | $8505.07      |
| Mar   | 01  | 2020 | $6424.35      |
| Apr   | 01  | 2020 | $8624.28      |
| May   | 01  | 2020 | $9446.57      |
| Jun   | 01  | 2020 | $9136.20      |
| Jul   | 01  | 2020 | $11351.62     |
| Aug   | 01  | 2020 | $11655.00     |
| Sep   | 01  | 2020 | $10779.63     |
| Oct   | 01  | 2020 | $13804.81     |
| Nov   | 01  | 2020 | $19713.94     |
| Dec   | 01  | 2020 | $28990.08     |

In this section, we use a smaller data set to keep things simple for now. We
will use the MM/DD/YY format in the subsequent examples and expand on this data
set later on to include 2021 and 2022 monthly market prices as well.

## Defining Data Sets

### Defining Record Entries

Our columns will be the following: Date, Market Price, Principal Amount, Target
Value, Current Value, Order Size, Total Order Size, and Interval.

-   **Date** represents the date for the current record (row).
-   **Market Price** represents the current price at which each unit of Bitcoin
    was bought or sold.
-   **Principal Amount** represents the amount of money that was put into the
    investment.
-   **Target Value** represents our desired projected value for our current
    overall investment.
-   **Current Value** represents the most recent total value of our investment.
-   **Order Size** represents the amount that we purchased.
-   **Total Order Size** represents the total amount that we purchased.
-   **Interval** represents the total number of times we've invested.

_Principal Amount_ is the only _constant value_. A **constant value** is a
_fixed value_, meaning a value that does not change. The rest are _variables_. A
variable represents an unknown or yet to be calculated value. The variables will
be calculated based on whether certain _conditions_ are met.

Using small numbers and multiples of 10 tends to keep things simple. This allows
us to catch errors when we make mistakes, making them more apparent and easy to
backtrack. As a result, our _Principal Amount_ will be $10.

The _Market Price_ for the _Date_ Jan 01, 2020 was $9334.98.

The following is the outline for our first record entry:

| Date     | Market Price | Current Target | Current Value | Principal Amount | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     |                |               | $10              |            |                  |             |

This allows us to set up our first record.

### Setting Up the Initial Record Entry

We also need to define how we will calculate the rest of the columns.

-   **Interval** = 1 + Interval
-   **Current Target** = Principal Amount \* Interval
-   **Order Size** = Principal Amount / Market Price
-   **Total Order Size** = Order Size + Previous Total Order Size
-   **Current Value** = Market Price \* Previous Total Order Size

-   If there is no **Previous Total Order Size**, then set **Pervious Total
    Order Size** to **0**.
-   If there is no previous **Interval**, then set **Interval** to **0**.

Let's start by setting both _Previous Total Order Size_ and _Interval_ to 0.

-   **Previous Total Order Size** = 0
-   **Interval** = 0

Now we can calculate our _Current Target_, _Current Value_, _Order Size_, and
_Interval_.

-   **Interval** = 1 + 0 = 1
-   **Current Target** = 10 \* 1 = 10
-   **Order Size** = 10 / 9334.98 ≈ 0.00107124
-   **Total Order Size** = 0.00107124 + 0 ≈ 0.00107124
-   **Current Value** = 9334.98 \* 0 = 0

The following would be the result for our first record entry:

| Date     | Market Price | Current Target | Current Value | Principal Amount | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |

It's important to keep in mind that **Current Value** evaluates to **0** because
_we had no previous investment_. This will only ever be true for the first
record entry while operating under the assumption that the investment remains
_solvent_.

### Calculating and Recording the Second Record Entry

Let's create the second record to see how each cell is evaluated and then
recorded.

| Date     | Market Price | Current Target | Current Value | Principal Amount | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     |                |               | $10              |            |                  |             |

All we have to do is follow the same pattern as before while updating each
variable using the given information.

-   **Interval** = 1 + 1 = 2
-   **Current Target** = 10 \* 2 = 20
-   **Order Size** = 10 / 8505.07 ≈ 0.00117577
-   **Total Order Size** = 0.00117577 + 0.00107124 ≈ 0.00224701
-   **Current Value** = 8505.07 \* 0.00107124 = 9.11

| Date     | Market Price | Current Target | Current Value | Principal Amount | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     | $20            | $9.11         | $10              | 0.00117577 | 0.00224701       | 2           |

We follow these steps every time we invest from this point forward and never
deviate from the investment plan.

### Adding Columns to a Table

This table isn't displaying our gain or loss. Let's define a new expression to
evaluate our gain or loss in a new column. We can place it in between our
**Current Value** and **Principal Amount** columns.

-   **Gain or (Loss)** = Current Value - Previous Current Target

-   If there is no **Current Value**, then set **Current Value** to **0**.
-   If there is no **Previous Current Target**, then set **Previous Current
    Target** to **0**.

-   A **Gain** is represented as a _positive value_ (+) while a **Loss** is
    represented as a _negative value_ (-).

-   First Row: **Gain or (Loss)** = 0 - 0 = 0
-   Second Row: **Gain or (Loss)** = 9.11 - 10 ≈ -0.89

| Date     | Market Price | Current Target | Current Value | Gain or (Loss) | Principal Amount | Order Size | Total Order Size | Interval |
| -------- | ------------ | -------------- | ------------- | --------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | 0         | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     | $20            | $9.11         | -$0.89    | $10              | 0.00117577 | 0.00224701       | 2           |

## Summary

In this specification, we focused on managing data related to Dollar-Cost
Averaging for Bitcoin investment. We started by gathering a sample dataset
containing the closing prices of Bitcoin for the first day of each month
in 2020. Then, we defined and initialized a table to track our investment
progress, including columns for Date, Market Price, Principal Amount, Current
Target, Current Value, Order Size, Total Order Size, and Interval.

Afterward, we demonstrated how to create new records and calculate the values
for each column. We also added a Gain or (Loss) column to display the difference
between the current value and the previous target value. This approach allows us
to track our investment progress and ensure that we follow a consistent
strategy, such as providing insights into our gains or losses over time. By
following this data management method, we can make more informed decisions and
maintain a disciplined investment plan.

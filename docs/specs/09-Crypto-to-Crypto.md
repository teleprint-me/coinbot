# Crypto-to-Crypto Transaction Breakdown

Crypto-to-Crypto transaction steps for each side using `LTC-BTC` as the given product.

## Structure

             Product                 LTC-BTC
                |                       |
          +-----+-----+           +-----+-----+
          |           |           |           |
         Base       Quote        LTC         BTC
          |           |           |           |
        Base        Quote      LTC-USD     BTC-USD
        Product     Product

- Left (Product tree) is Abstract.

- Right (LTC-BTC tree) is Concrete.

## Abstract

psuedocode:

```plaintext
# Buy Side
IF transaction.side is BUY
THEN
    missing transaction
        sold quote for fiat AND bought base with fiat

# Sell Side
IF transaction.side is SELL
THEN
    missing transaction
        sold base for fiat AND bought quote with fiat
```

Example:

| BUY              | SELL             |
| ---------------- | ---------------- |
| Buy LTC with BTC | Sell LTC for BTC |
| Sell BTC for USD | Sell LTC for USD |
| Buy LTC with USD | Buy BTC with USD |

## Concrete Examples

### BUY Side Transaction Details

The following is a fully broken down transaction.

| Property   | Value                    |
| ---------- | ------------------------ |
| portfolio  | default                  |
| trade_id   | 11704338                 |
| product    | LTC-BTC                  |
| side       | BUY                      |
| created_at | 2021-10-20T02:46:56.008Z |
| size       | Ł0.01699112              |
| size_unit  | LTC                      |
| price      | ₿0.002928                |
| fee        | ₿0.00000025              |
| total      | ₿0.00005000              |
| total_unit | BTC                      |

Where

| Property   | Value                                             |
| ---------- | ------------------------------------------------- |
| size       | Order Size for Litecoin                           |
| size_unit  | The Base Product                                  |
| price      | Market Price in Bitcoin for each unit of Litecoin |
| fee        | Order Fee in Bitcoin                              |
| total      | Amount purchased in Bitcoin                       |
| total_unit | The Quote Product                                 |

### Calculate product for BUY side

1.  Determine the Product, Base Product, and Quote Product.

    -   Product is Bought, e.g. LTC-BTC
    -   Base Product is Bought, e.g. LTC-USD
    -   Quote Product is Sold, e.g. BTC-USD

    psuedocode:

    ```plaintext
    base_product = transaction.size_unit

    quote_product = transaction.total_unit
    ```

2.  Determine Market Price for BTC-USD and LTC-USD using `transaction.created_at` transaction property.

    Note: this function makes REST API calls.

    psuedocode:

    ```plaintext
    base_response = get_spot_price(base_product, transaction.created_at)
    base_price = base_response["data"]["amount"]
    base_price = $188.73

    quote_response = get_spot_price(quote_product, transaction.created_at)
    quote_price = quote_response["data"]["amount"]
    quote_price = $64303.14
    ```

    example:

    ```sh
    >>> base_response = get_spot_price(base_product, transaction.created_at)
    >>> base_response
    {'data': {'base': 'LTC', 'currency': 'USD', 'amount': '188.73'}}
    ```

3.  Determine the Transaction Total for both Base Product and Quote Product.

    psuedocode:

    ```plaintext
    base_total = base_price * transaction.size
    base_total = $188.73 * Ł0.01699112
    base_total ≅ $3.206

    quote_total = quote_price * transaction.total
    quote_total = $64303.14 * ₿0.00005000
    quote_total ≅ $3.215
    ```

4.  Determine the Transaction Fee for both Base Product and Quote Product.

    Note: The fee is only ever determined once (e.g. LTC-BTC) and is calculated by the Quote Product because this is the product that we either buy or sell with. This means that we only calculate the quote_fee and leave the base_fee zeroed out.

    psuedocode:

    ```plaintext
    quote_fee = quote_price * transaction.fee
    quote_fee = $64303.14 * ₿0.00000025
    quote_fee ≅ $0.016

    base_fee = 0.00
    ```

    Taking the difference between the quote_total and base_total should validate our assumption the transaction fee cost.

    ```plaintext
    estimated_fee = quote_total - base_total
    estimated_fee ≅ $3.215 - $3.206
    estimated_fee ≅ 0.00899

    estimated_base = quote_total - quote_fee
    estimated_base ≅ 3.215 - 0.016
    estimated_fee ≅ 3.199
    ```

    Not exact, but close enough.

5.  Next we have to get the size for the Base Product and Quote Product.

    psuedocode:

    ```plaintext
    base_size = transaction.size
    base_size = Ł0.01699112

    quote_size = transaction.total
    quote_size = ₿0.00005000
    ```

6.  The last step is to label each product transaction.

    psuedocode:

    ```plaintext
    base_side = BUY

    quote_side = SELL
    ```

### SELL Side Transaction Details

The following is a fully broken down transaction.

| Property   | Value                    |
| ---------- | ------------------------ |
| portfolio  | default                  |
| trade_id   | 10866959                 |
| product    | LTC-BTC                  |
| side       | SELL                     |
| created_at | 2021-06-26T03:42:15.349Z |
| size       | Ł0.10000000              |
| size_unit  | LTC                      |
| price      | ₿0.003965                |
| fee        | ₿0.00000198              |
| total      | ₿0.00039452              |
| total_unit | BTC                      |

Where

| Property   | Value                                             |
| ---------- | ------------------------------------------------- |
| size       | Order Size for Litecoin                           |
| size_unit  | The Base Product                                  |
| price      | Market Price in Bitcoin for each unit of Litecoin |
| fee        | Order Fee in Bitcoin                              |
| total      | Amount purchased in Bitcoin                       |
| total_unit | The Quote Product                                 |

### Calculate product for SELL side

1.  Determine the Product, Base Product, and Quote Product.

    -   Product is Sold, e.g. LTC-BTC
    -   Base Product is Sold, e.g. LTC-USD
    -   Quote Product is Bought, e.g. BTC-USD

    psuedocode:

        base_product = transaction.size_unit

        quote_product = transaction.total_unit

2.  Determine Market Price for BTC-USD and LTC-USD using `transaction.created_at` transaction property.

    Note: this function makes REST API calls.

    psuedocode:

    ```plaintext
    base_response = get_spot_price(base_product, transaction.created_at)
    base_price = base_response["data"]["amount"]
    base_price = $124.97

    quote_response = get_spot_price(quote_product, transaction.created_at)
    quote_price = quote_response["data"]["amount"]
    quote_price = $31594.62
    ```

    example:

    ```sh
    >>> transaction = CoinbaseProTransaction(
    ...     portfolio="default",
    ...     trade_id="10866959",
    ...     product="LTC-BTC",
    ...     side="SELL",
    ...     created_at="2021-06-26T03:42:15.349Z",
    ...     size=0.10000000,
    ...     size_unit="LTC",
    ...     price=0.003965,
    ...     fee=0.0000019825,
    ...     total=0.0003945175,
    ...     total_unit="BTC",
    ...     notes="Converted 0.10000000 LTC to 0.0003945175 BTC"
    ... )
    >>> base_product
    'LTC-USD'
    >>> quote_product
    'BTC-USD'
    >>> base_response = get_spot_price(base_product, transaction.created_at)
    >>> quote_response = get_spot_price(quote_product, transaction.created_at)
    >>> base_response
    {'data': {'base': 'LTC', 'currency': 'USD', 'amount': '124.97'}}
    >>> quote_response
    {'data': {'base': 'BTC', 'currency': 'USD', 'amount': '31594.62'}}
    >>> base_price = base_response["data"]["amount"]
    >>> base_price
    '124.97'
    >>> quote_price = quote_response["data"]["amount"]
    >>> quote_price
    '31594.62'
    ```

3.  Determine the Transaction Total for both Base Product and Quote Product.

    psuedocode:

    ```plaintext
    base_total = base_price * transaction.size
    base_total = $124.97 * Ł0.10000000
    base_total ≅ $12.497

    quote_total = quote_price * transaction.total
    quote_total = $31594.62 * ₿0.0003945175
    quote_total ≅ $12.465
    ```

    example:

    ```shell
    >>> base_total = float(base_price) * transaction.size
    >>> base_total
    12.497000000000003
    >>> quote_total = float(quote_price) * transaction.total
    >>> quote_total
    12.4528717975
    ```

4.  Determine the Transaction Fee for both Base Product and Quote Product.

    Note: The fee is only ever determined once (e.g. LTC-BTC) and is calculated by the Quote Product because this is the product that we either buy or sell with. This means that we only calculate the quote_fee and leave the base_fee zeroed out.

    psuedocode:

    ```plaintext
    quote_fee = quote_price * transaction.fee
    quote_fee ≅ $31594.62 * ₿0.00000198
    quote_fee ≅ $0.063

    base_fee = 0.00
    ```

    example:

    ```plaintext
    >>> quote_fee = float(quote_price) * transaction.fee
    >>> quote_fee
    0.06263633415
    >>> base_fee = 0.00
    ```

5.  Next we have to get the size for the Base Product and Quote Product.

    psuedocode:

    ```plaintext
    base_size = transaction.size
    base_size = Ł0.10000000

    quote_size = transaction.total
    quote_size ≅ ₿0.00039452
    ```

6.  The last step is to label each product transaction.

    psuedocode:

    ```plaintext
    base_side = SELL

    quote_side = BUY
    ```

## Summary

### Context

We have a CSV file containing Coinbase Pro transactions. We need to use these transactions to calculate the missing transactions for any crypto-to-crypto transactions. For example, if there is a transaction for buying Litecoin (LTC) with Bitcoin (BTC), we need to calculate the corresponding transaction of selling BTC for USD and then buying LTC with USD.

### Problem

We need to calculate the missing transaction details for any crypto-to-crypto transactions in the CSV file.

### Solution

1. Determine the Product, Base Product, and Quote Product.

    - For a BUY transaction:

        - Product is Bought, e.g. LTC-BTC
        - Base Product is Bought, e.g. LTC-USD
        - Quote Product is Sold, e.g. BTC-USD

    - For a SELL transaction:
        - Product is Sold, e.g. LTC-BTC
        - Base Product is Sold, e.g. LTC-USD
        - Quote Product is Bought, e.g. BTC-USD

2. Determine Market Price for BTC-USD and LTC-USD using transaction.created_at transaction property. Note: this function makes REST API calls.

3. Determine the Transaction Total for both Base Product and Quote Product.

4. Determine the Transaction Fee for both Base Product and Quote Product.

    Note: The fee is only ever determined once (e.g. LTC-BTC) and is calculated by the Quote Product because this is the product that we either buy or sell with.

5. Get the size for the Base Product and Quote Product.

6. Label each product transaction as a BUY or SELL.

Once the missing transaction details have been calculated, create two CoinbaseProTransaction objects - one for the BUY transaction and another for the SELL transaction. These objects will contain the following details:

-   Portfolio
-   Trade ID
-   Product
-   Side (BUY or SELL)
-   Size
-   Size Unit
-   Price
-   Fee
-   Total
-   Total Unit
-   Notes

Finally, add these CoinbaseProTransaction objects to the list of transactions.

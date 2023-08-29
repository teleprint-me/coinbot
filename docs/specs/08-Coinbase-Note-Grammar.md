# Coinbase Note Grammar

## Part 1

Let's take a look at some notes for examples and see how you think they should be structured.

Example (Coinbase notes sample set):

Let's first consider the original transaction records as a CSV, `list[list[str]]`, that will fit the criteria for our context. Then we can cover each case individually.

Here is a sample data set for Coinbase Transactions:

```py
['Timestamp', 'Transaction Type', 'Asset', 'Quantity Transacted', 'Spot Price Currency', 'Spot Price at Transaction', 'Subtotal', 'Total (inclusive of fees and/or spread)', 'Fees a
nd/or Spread', 'Notes']
['2020-06-16T19:21:02Z', 'Buy', 'BTC', '0.00094589', 'USD', '9525.42', '9.01', '10.00', '0.990000', 'Bought 0.00094589 BTC for $10.00 USD']
['2020-07-23T18:50:22Z', 'Send', 'BTC', '0.00188372', 'USD', '9586.08', '', '', '', 'Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih']
['2020-10-03T00:27:45Z', 'Receive', 'BTC', '0.00321806', 'USD', '10545.34', '', '', '', 'Received 0.00321806 BTC from an external account']
['2021-12-23T21:14:49Z', 'Receive', 'BTC', '4.92e-06', 'USD', '50781.68', '', '', '', 'Received 0.00000492 BTC from Coinbase Card']
['2022-02-08T03:38:51Z', 'Advanced Trade Buy', 'BTC', '0.00045096', 'USD', '44110.19', '19.89', '19.99', '0.099460', 'Bought 0.00045096 BTC for $19.99 USD on BTC-USD']
['2022-09-16T23:38:22Z', 'CardSpend', 'BTC', '0.0005142', 'USD', '19622.71', '', '', '', 'xxxxxxxxxxxxxxxxxxxx68dd']
['2022-05-15T00:23:51Z', 'Convert', 'USDC', '9.4', 'USD', '1.00', '8.35', '9.40', '1.05', 'Converted 9.4000 USDC to 0.00027696 BTC']
['2020-10-01T16:38:37Z', 'Learning Reward', 'MKR', '0.0035332', 'USD', '568.91', '2.01', '2.01', '0.00', 'Received 0.0035332 MKR from Coinbase as a learning reward']
['2022-06-05T04:33:00Z', 'Rewards Income', 'USDC', '0.004247', 'USD', '1.00', '0.00', '0.00', '0.00', 'Received 0.004247 USDC from Coinbase Rewards']
['2022-01-18T20:18:43Z', 'Sell', 'USDC', '2.3', 'USD', '1.00', '2.30', '2.30', '0.00', 'Sold 2.3000 USDC for $2.30 USD']
['2022-03-20T21:03:19Z', 'Advanced Trade Sell', 'DAI', '1.15839', 'USD', '1.00', '1.16', '1.16', '0.000116', 'Sold 1.15839 DAI for $1.16 USD on DAI-USD']
['2022-02-03T05:17:36Z', 'Convert', 'LTC', '0.30241992', 'USD', '108.00', '32.02', '32.66', '0.640000', 'Converted 0.30241992 LTC to 0.00086634 BTC']
['2022-04-20T23:06:08Z', 'Convert', 'LINK', '0.00749', 'USD', '14.69', '0.100000', '0.110000', '0.010000', 'Converted 0.00749 LINK to 0.00000248 BTC']
['2022-04-20T23:07:01Z', 'Convert', 'EOS', '0.0875', 'USD', '2.74', '0.240000', '0.240000', '0.00', 'Converted 0.0875 EOS to 0.00000571 BTC']
```

Sample Context. We can think of a Coinbase Note as meta data about a given recorded transaction. The majority of Coinbase Notes are Verb Phrases indicating some type of context based on what happened with which transaction.

Sample Problem. We need to convert Coinbase Notes to a given expected grammer. The grammer may cover 3 possible structures, but each grammer will follow a similar or related structure, even if the transactions are not identical.

1. The Coinbase Note string may be an address and nothing else.

There is a record that looks like the following: `['2022-09-16T23:38:22Z', 'CardSpend', 'BTC', '0.0005142', 'USD', '19622.71', '', '', '', 'xxxxxxxxxxxxxxxxxxxx68dd']`.

This record contains the notes column value of `xxxxxxxxxxxxxxxxxxxx68dd` where `x` is the censored address; The uncensored address would consist of a valid hash sum. This note is an example of a Coinbase Note with a single token where that token represents an address or code of some type (currently unknown and unutilized).

We can represent that address with a new grammar where that grammar is "DETERMINER" where the given notes address is the determiner.

We can then create a CoinbaseNote object with this grammar by assigning the given transaction record accordingly by extracting and converting relevant information appropriately.

```py
CoinbaseNote(
    determiner="xxxxxxxxxxxxxxxxxxxx68dd",  # extracted notes from transaction record
    product="BTC-USD",  # extracted base and quote from transaction record
    transaction_type="Send",  # extracted from transaction record
)
```

2. The Coinbase Note string may contain relevant information about an action taken. We can think of this as a verb phrase. These transactions usually involved some kind of trade action such as "Bought" , "Sold", or "Converted".

Examples of this would be the following:

```py
['2020-06-16T19:21:02Z', 'Buy', 'BTC', '0.00094589', 'USD', '9525.42', '9.01', '10.00', '0.990000', 'Bought 0.00094589 BTC for $10.00 USD']
['2022-01-18T20:18:43Z', 'Sell', 'USDC', '2.3', 'USD', '1.00', '2.30', '2.30', '0.00', 'Sold 2.3000 USDC for $2.30 USD']
['2022-05-15T00:23:51Z', 'Convert', 'USDC', '9.4', 'USD', '1.00', '8.35', '9.40', '1.05', 'Converted 9.4000 USDC to 0.00027696 BTC']
```

This record contains the notes column value of `Bought 0.00094589 BTC for $10.00 USD` where the verb phrase is `VERB SIZE BASE PREPOSITION DETERMINER QUOTE`. We should be able to match this grammar with any Coinbase Note that follows this grammar.

We can then create a CoinbaseNote object with this grammar by assigning the given transaction record accordingly by extracting and converting relevant information appropriately.

```py
CoinbaseNote(
    verb="Bought",
    size="0.00094589",
    base="BTC",
    preposition="for",
    determiner="$10.00",
    quote="USD",
    product="BTC-USD",
    transaction_type="Buy",
)
```

3. The last type of grammar is the trickiest because there is no QUOTE and the DETERMINER is of a variable size or length. The third type of grammar can be thought of as any transaction note that does not have a single address as the note and is a note that does not contain a transaction type of "Bought" , "Sold", or "Converted" within its grammar.

Examples of this would be the following:

```py
['2020-07-23T18:50:22Z', 'Send', 'BTC', '0.00188372', 'USD', '9586.08', '', '', '', 'Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih']
['2020-10-03T00:27:45Z', 'Receive', 'BTC', '0.00321806', 'USD', '10545.34', '', '', '', 'Received 0.00321806 BTC from an external account']
```

We can look at the transaction `Received 0.00321806 BTC from an external account` to get a feeling for this and analyzing its grammar. This notes grammar consists of the following: `VERB SIZE BASE PREPOSITION DETERMINER` which differs from grammars 1 and 2 respectively. It is the last and final potential grammar structure.

We can then create a CoinbaseNote object with this grammar by assigning the given transaction record accordingly by extracting and converting relevant information appropriately.

```py
CoinbaseNote(
    verb="Recieved",
    size="0.00321806",
    base="BTC",
    preposition="from",
    determiner="from an external account",
    product=="BTC",
    transaction_type=transaction_type,
)
```

Let's take a look at some notes for examples and see how you think they should be structured given this context.

Solve for the following given samples:

Coinbase Notes (Samples):

1. "Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih"

2. "Converted 9.4000 USDC to 0.00027696 BTC"

What should the grammar for the given Coinbase Notes strings look like when creating a `CoinbaseNote`? What would the instantiation of each `CoinbaseNote` look like for each one. Given the solution according to the given format by referencing and summaring each problem and then explain why your given solution for each problem is accurate according to the context at hand.

## Part 2

Let's simplify the expected grammars and their associated structures.

Sample Context: We can think of a Coinbase Note as meta data about a given recorded transaction. The majority of Coinbase Notes are Verb Phrases indicating some type of context based on what happened with which transaction.

Sample Problem: We need to convert Coinbase Notes to a given expected grammer. The grammer may cover 3 possible structures, but each grammer will follow a similar or related structure, even if the transactions are not identical.

1. The Address Grammar Type.

Address Grammar:

```md
a. Description: The `Address Grammar` always consists of a single token.
b. Grammar: `DETERMINER`
c. Sample: "xxxxxxxxxxxxxxxxxxxx68dd"
```

Address Record:

```py
['2022-09-16T23:38:22Z', 'CardSpend', 'BTC', '0.0005142', 'USD', '19622.71', '', '', '', 'xxxxxxxxxxxxxxxxxxxx68dd']`
```

Address Note:

```py
# `x` is the censored address where the
# uncensored address would consist of a valid hash sum.
# Notes string following the grammar of type "DETERMINER"
"xxxxxxxxxxxxxxxxxxxx68dd"
```

Instantiating `CoinbaseNote` using `Address Grammar`:

```py
CoinbaseNote(
    determiner="xxxxxxxxxxxxxxxxxxxx68dd",  # extracted notes from transaction record
    product="BTC-USD",  # extracted base and quote from transaction record
    transaction_type="Send",  # extracted from transaction record
)
```

2. The Trade Grammar Type.

Trade Grammar:

```md
a. Description: The `Trade Grammar` always consists of 6 tokens.
b. Grammar: `VERB SIZE BASE PREPOSITION DETERMINER QUOTE`
c. Sample: "Bought 0.00094589 BTC for $10.00 USD"
```

Trade Record:

```py
['2022-05-15T00:23:51Z', 'Convert', 'USDC', '9.4', 'USD', '1.00', '8.35', '9.40', '1.05', 'Converted 9.4000 USDC to 0.00027696 BTC']
```

Trade Note:

```py
# Notes string following the grammar of type
# "VERB SIZE BASE PREPOSITION DETERMINER QUOTE"
"Converted 9.4000 USDC to 0.00027696 BTC"
```

Instantiating `CoinbaseNote` using `Trade Grammar`:

```py
CoinbaseNote(
    verb="Convert",
    size="9.4000",
    base="USDC",
    preposition="to",
    determiner="0.00027696",
    quote="BTC",
    product="USDC-BTC",
    transaction_type="Buy",
)
```

3. The Transaction Grammar Type.

Transaction Grammar:

```md
a. Description: The `Transaction Grammar` always consists of 5 or more tokens; The number of `DETERMINER` tokens is unknown in advance and they are merged into a single token.
b. Grammar: `VERB SIZE BASE PREPOSITION DETERMINER`
c. Sample: "Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih"
```

Transaction Record:

```py
['2020-10-03T00:27:45Z', 'Receive', 'BTC', '0.00321806', 'USD', '10545.34', '', '', '', 'Received 0.00321806 BTC from an external account']
```

Transaction Note:

```py
# Notes string following the grammar of type
# "VERB SIZE BASE PREPOSITION DETERMINER"
"Received 0.00321806 BTC from an external account"
```

Instantiating `CoinbaseNote` using `Transaction Grammar`:

```py
CoinbaseNote(
    verb="Recieved",
    size="0.00321806",
    base="BTC",
    preposition="from",
    determiner="from an external account",
    product=="BTC",
    transaction_type=transaction_type,
)
```

Let's take a look at some notes for examples and see how you think they should be structured given this context.

Solve for the following given samples:

Coinbase Notes (Samples):

1. "Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih"

2. "Converted 9.4000 USDC to 0.00027696 BTC"

What should the grammar for the given Coinbase Notes strings look like when creating a `CoinbaseNote`? What would the instantiation of each `CoinbaseNote` look like for each one. Given the solution according to the given format by referencing and summaring each problem and then explain why your given solution for each problem is accurate according to the context at hand.

## Part 3

The problem is that the `DETERMINER` was either not tokenized correctly during scanning or `CoinbaseNote` was not instantiated correctly. Either is possible.

Here is the current instance:

```py
CoinbaseNote(
    verb='Bought',
    size='0.00094589',
    base='BTC',
    preposition='for',
    determiner='$10.00 USD',
    quote='',
    product='BTC',
    transaction_type='Buy'
)
```

The `Trade Grammar` uses the following structure: `VERB SIZE BASE PREPOSITION DETERMINER QUOTE`.

The given note has the following string: "Bought 0.00094589 BTC for $10.00 USD".

`DETERMINER` should be `$10.00` and `QUOTE` should be `USD`.

We can map the grammar type to the string to see if it fits the expected `Trade Gammar` type.

| Token Key   | Token Value |
| ----------- | ----------- |
| VERB        | Bought      |
| SIZE        | 0.00094589  |
| BASE        | BTC         |
| PREPOSITION | for         |
| DETERMINER  | $10.00      |
| QUOTE       | USD         |

Instead we have a bug because the output is not as expected according to the given grammar. This leaves us with the `DETERMINER` being set to `$10.00 USD` and `QUOTE` being set to `''`.

| Token Key   | Token Value |
| ----------- | ----------- |
| VERB        | Bought      |
| SIZE        | 0.00094589  |
| BASE        | BTC         |
| PREPOSITION | for         |
| DETERMINER  | $10.00 USD  |
| QUOTE       | ''          |

The issue with the given `CoinbaseNote` instance might be that the tokens aren't being created properly and or the tokens are being assigned to the wrong properties as a result.

The grammar used in this instance is for the `Trade Grammar`, but the determiner value provided does not match the expected format of a currency value, as it includes the currency name. The determiner value should only include the currency value as the original string value and the quote value should only include currency code.

To fix the issue, the determiner value should be changed to '$10.00' and the quote value should be set to 'USD'.

The correct grammar for the given `Trade Gammar` should map accordingly:

| Token Key   | Token Value |
| ----------- | ----------- |
| VERB        | Bought      |
| SIZE        | 0.00094589  |
| BASE        | BTC         |
| PREPOSITION | for         |
| DETERMINER  | $10.00      |
| QUOTE       | USD         |

The correct instantiation of the `CoinbaseNote` instance using the `Trade Grammar` should look like the following:

```py
CoinbaseNote(
    verb='Bought',
    size='0.00094589',
    base='BTC',
    preposition='for',
    determiner='$10.00',
    quote='USD',
    product='BTC-USD',
    transaction_type='Buy'
)
```

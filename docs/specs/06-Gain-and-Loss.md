# Gains and Losses

Capital gains and losses refer to the profit or loss realized from the sale or
exchange of a capital asset, such as stocks, bonds, or real estate. A capital
gain occurs when the sale price is higher than the purchase price, while a
capital loss occurs when the sale price is lower than the purchase price. The
amount of capital gains or losses to report on a tax return depends on various
factors.

# How to Calculate Gains and Losses - Algorithm

1. Structure the dataset for scanning and parsing. Scanning will consist of
   reading and structuring a given dataset. Parsing will consist of calculating
   the given dataset.

    - `GLTransaction` has the following mutable fields:

        - `GLTransaction.additional_description`
        - `GLTransaction.description`
        - `GLTransaction.date_acquired`
        - `GLTransaction.transaction_type`
        - `GLTransaction.order_size`
        - `GLTransaction.market_price`
        - `GLTransaction.exchange_fee`
        - `GLTransaction.cost_or_other_basis`
        - `GLTransaction.acb_per_share`
        - `GLTransaction.date_sold`
        - `GLTransaction.sales_proceeds`
        - `GLTransaction.gain_or_loss`

    - `GLTransaction` has the following immutable properties:

        - `GLTransaction.is_buy`
        - `GLTransaction.is_sell`

2. Scan and aggregate all related transactions.

    - Read all available datasets from a set of given source transactions; This
      is a directory path containing all related CSV transaction datasets.

    - The dataset is converted into a `list` of `IRTransaction` (Intermediary
      Representation Transaction) instances.

    - The `list` of `IRTransaction` instances is converted to a `list` of
      `GLTransaction` (Gains and Losses Transaction) instances.

    - Return the list of `GLTransaction` instances.

3. Parse and calculate the given aggregated datasets.

    - Parse the dataset into a `list` named `transaction_block` where each
      `block` is a `list` of `GLTransaction` instances of a single
      `transaction_type`.

        - A `transaction_block` is a `list` of `list` of `GLTransaction`
          instances representing continguous sets of sequences of related
          transactions.

        - A `transaction_block` will only ever contain `list` of sequences of
          either Buy or Sell transactions representing their original sequence
          of execution.

        - A `block` is a `list` of `GLTransaction` instances representing a
          single, continguous, sequence of related transactions.

        - A `block` must only ever contain a single `transaction_type` with a
          given sequence.

4. Implement variables to handle tracking totals for `order_size` and
   `cost_or_other_basis`.

    - The following variables track the overall running total:

        - All other calculations depend on these calculations being as accurate
          and reliable as possible.

            - `total_order_size = 0`
            - `total_cost_basis = 0`
            - `total_acb_per_share = 0`

        - These variables can never be reset as it may skew or distort all other
          calculations that succeed them.

            - If `block[0].is_buy`, Then

                - Calculate overall running totals.

                    - `total_order_size += sum(tx.order_size for tx in block)`
                    - `total_cost_basis += sum(tx.cost_or_other_basis for tx in block)`

            - Else `block[0].is_sell`, Then

                - Calculate overall running totals using additive inverse
                  property.

                    - `total_order_size += sum(-tx.order_size for tx in block)`
                    - `total_cost_basis += sum(-tx.cost_or_other_basis for tx in block)`

        - Use the ratio between the `total_cost_or_other_basis` and
          `total_order_size` to calculate the `total_acb_per_share` for a given
          `transaction_block`.

            - `total_acb_per_share = total_cost_or_other_basis / total_order_size`

            - The `total_acb_per_share` is used to perform calculations with
              `GLTransaction` instances.

5. Parse `GLTransaction` calcuations.

    - We must evaluate the right calculations at the right times; Calculations
      must be evaluated in an imperative fashion.

    - For each `block` within a `transaction_block`

        - We first calculate all the prerequisite values for each block which
          either represents a sequence of Buy `transaction_type` or Sell
          `transaction_type`.

        - For each `transaction` within a `block`

            - If `transaction.is_buy`, Then

                - Calculate `transaction.cost_or_other_basis`

                    - `order_size = transaction.order_size`
                    - `market_price = transaction.market_price`
                    - `exchange_fee = transaction.exchange_fee`
                    - `cost_basis = (order_size * market_price) + exchange_fee`
                    - `transaction.cost_or_other_basis = cost_basis`

                - Calculate `transaction.acb_per_share`

                    - NOTE: This is only ever used with a Buy
                      `transaction_type`. The Sell `transaction_type` always
                      inherits its `acb_per_share` value from the last known
                      `total_acb_per_share`.

                    - `order_size = transaction.order_size`
                    - `cost_basis = transaction.cost_or_other_basis`
                    - `transaction.acb_per_share = cost_basis / order_size`

            - Else `transaction.is_sell`, Then

                - Inherit last calculated `total_acb_per_share` value.

                    - `transaction.acb_per_share = total_acb_per_share`

                - Caclulate `transaction.cost_or_other_basis`

                    - `order_size = transaction.order_size`
                    - `acb_per_share = transaction.acb_per_share`
                    - `transaction.cost_or_other_basis = order_size * acb_per_share`

                - Calculate `transaction.sales_proceeds`

                    - `order_size = transaction.order_size`
                    - `market_price = transaction.market_price`
                    - `transaction.sales_proceeds = order_size * market_price`

                - Calculate `transaction.gain_or_loss`

                    - `sales_proceeds = transaction.market_price`
                    - `cost_basis = transaction.cost_or_other_basis`
                    - `exchange_fee = transaction.exchange_fee`
                    - `transaction.gain_or_loss = sales_proceeds - cost_basis - exchange_fee`

        - Calculate `total_cost_or_other_basis`, `total_order_size`, and
          `total_acb_per_share`.

            - `total_order_size` represents the sum of the `order_size` column
              for the current `transaction_block`.

            - If `block[0].is_buy`, Then

                - Calculate overall running totals.

                    - `total_order_size += sum(tx.order_size for tx in block)`
                    - `total_cost_basis += sum(tx.cost_or_other_basis for tx in block)`

            - Else `block[0].is_sell`, Then

                - Calculate overall running totals using additive inverse
                  property.

                    - `total_order_size += sum(-tx.order_size for tx in block)`
                    - `total_cost_basis += sum(-tx.cost_or_other_basis for tx in block)`

            - Calculate the `total_acb_per_share`

                - `total_acb_per_share = total_cost_or_other_basis / total_order_size`

            - Create a new `GLTransaction` instance containing the totaled
              calculations.

        - Extend the `list` of `GLTransaction` instances.

        - Append the newly created `GLTransaction` instance to the `list` of
          `GLTransaction` instances.

    - Return the processed `list` of `GLTransaction` instances.

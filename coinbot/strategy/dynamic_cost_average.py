"""
Module: coinbot.strategy.dca
Description: Dynamic Cost Averaging

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
"""

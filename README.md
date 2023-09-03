# CoinBot

CoinBot: Automated Trading with Compound Interest Strategy

## Disclaimer

    I am a programmer and NOT an accredited financial expert.
    For important investment decisions, consult a certified financial professional.
    Do NOT rely on investment advice from anonymous sources online; always conduct thorough research.

📝 THIS SOFTWARE IS UNDER ACTIVE DEVELOPMENT AND IS SUBJECT TO CHANGE

⚠️ USE THIS SOFTWARE AT YOUR OWN RISK!

🚨 ALWAYS AUDIT THE OUTPUT!

## About CoinBot

CoinBot is a project aimed at providing automated trading with a compound
interest strategy.

## Usage

### Hello, World!

```sh
23:39:41 | ~/Documents/code/remote/coinbot
(.venv) git:(main | Δ) λ python -m coinbot.xor
Epoch 0, Loss: 1.2193738304196795
Epoch 1000, Loss: 0.13607794952566488
Epoch 2000, Loss: 0.029654949330373555
Epoch 3000, Loss: 0.011085021961452618
Epoch 4000, Loss: 0.00614411595124679
Epoch 5000, Loss: 0.004098822486061569
Epoch 6000, Loss: 0.003024334504458357
Epoch 7000, Loss: 0.0023743844881101025
Epoch 8000, Loss: 0.0019434261038668197
Epoch 9000, Loss: 0.0016387396363412962
Predictions after training:
[[0.00219952]
 [0.94527828]
 [0.94887519]
 [0.00621378]]
```

### Simulation

The `simulate.py` script is designed to work with a single trade pair and blocks
if more than one trade pair is given, you can use the following commands to test
different scenarios:

1. **Basic Usage with Default Values**: This command will run the script with
   default values for the trade pair, timeframe, and other options.

   ```sh
   python -m coinbot.simulate
   ```

2. **Specify Trade Pair and Timeframe**: You can specify the trade pair (crypto
   symbols) and the timeframe for sampling. For example:

   ```sh
   python -m coinbot.simulate --symbols ETH/USD --timeframe 1H
   ```

3. **Specify Start and End Dates**: You can provide specific start and end dates
   for sampling. For example:

   ```sh
   python -m coinbot.simulate --start 2023-01-01 --end 2023-08-31
   ```

4. **Customize Principal and Rate**: You can adjust the principal amount and
   annual interest rate. For example:

   ```sh
   python -m coinbot.simulate --principal 500.00 --rate 0.15
   ```

5. **Change Frequency and Interval**: You can modify the compounding frequency
   and time step interval. For example:

   ```sh
   python -m coinbot.simulate --frequency 250 --interval 2
   ```

6. **Testing Error Handling**: You can test how the script handles errors by
   providing an invalid trade pair or missing required options:

   ```sh
   python -m coinbot.simulate --symbols INVALIDPAIR
   python -m coinbot.simulate --symbols BTC/USD --interval -1
   ```

7. **Example with All Options**: A more comprehensive command using various
   options:

   ```sh
   python -m coinbot.simulate --symbols LTC/USD --timeframe 15T --start 2023-07-01 --end 2023-07-15 --principal 1000.00 --rate 0.08 --frequency 180 --interval 3
   ```

Keep in mind that the script is designed for a single trade pair, so you can
experiment with different options to see how the script behaves under various
scenarios. Make sure to provide valid options to avoid triggering error
handling.

## License

    CoinBot: Automated Trading with Compound Interest Strategy
    Copyright (C) 2023 Austin Berrio

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

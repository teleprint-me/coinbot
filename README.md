# CoinBot: AI-Powered Trading Model

CoinBot is an AI-driven trading model designed to optimize trading decisions for
individual private treasuries. Utilizing advanced algorithms and historical data
analysis, CoinBot empowers traders with data-driven insights and responsive
trading capabilities.

## Disclaimer

    I am a programmer and NOT an accredited financial expert.
    For important investment decisions, consult a certified financial professional.
    Do NOT rely on investment advice from anonymous sources online; always conduct thorough research.

📝 THIS SOFTWARE IS UNDER ACTIVE DEVELOPMENT AND IS SUBJECT TO CHANGE

⚠️ USE THIS SOFTWARE AT YOUR OWN RISK!

🚨 ALWAYS AUDIT THE OUTPUT!

## Features

- **AI-Driven Insights**: Leverage AI for informed trading decisions based on
  market analysis.
- **Real-Time Trading**: Swiftly respond to market changes with CoinBot's
  real-time capabilities.
- **Diverse Asset Support**: Trade cryptocurrencies and stocks through Alpaca
  Markets API.
- **Customizable Strategies**: Tailor trading strategies to your risk tolerance
  and asset preferences.
- **Smart Portfolio Management**: Optimize portfolio allocation for returns and
  risk management.
- **Tailored Training**: Train CoinBot on your chosen assets to specialize its
  performance.

## Getting Started

Explore CoinBot's potential. Join in shaping AI-enhanced trading for individual
treasuries.

## Future Developments

Stay tuned for exciting updates, including advanced tax strategies, enhanced
risk management, and more.

## Usage

### CoinBot XOR Model

The CoinBot XOR model can be trained and utilized using the provided
command-line interface (CLI) script. Follow these steps to effectively use the
script:

#### Prerequisites

Make sure you have the necessary dependencies and a virtual environment set up.
Navigate to the `coinbot` directory where the `xor.py` script is located.

#### Training and Prediction

1. Open a terminal window.

2. Activate the virtual environment, if not already activated, to ensure proper
   package dependencies are used:

   ```sh
   poetry shell
   ```

3. Run the script using the following command:

   ```sh
   python -m coinbot.xor [OPTIONS]
   ```

   Replace `[OPTIONS]` with the desired command-line options described below.

#### Command-Line Options

The script supports various options to customize the training process and model
behavior. Use the following options to control the training process:

- `--model_id TEXT`: Specify the file path for the model. The default is
  `'models/coinbot-xor.h5'`.

- `--epochs INTEGER`: Set the number of training epochs. The default is 10,000.

- `--learning_rate FLOAT`: Set the learning rate for the training process. The
  default is 0.15.

- `--lambda_ FLOAT`: Set the L2 regularization parameter. The default is 1e-5.

- `--tolerance FLOAT`: Set the tolerance for early stopping during training. The
  default is 1e-5.

- `--help`: Display a help message with the options and their descriptions.

#### Customizing Training

To customize the behavior of the script and train the model with specific
parameters, use the command-line options. For example, to train the model with
different parameters:

```sh
python -m coinbot.xor --epochs 5000 --learning_rate 0.1
```

#### Output

During the training process, the script will display log messages indicating the
progress of the training. After training, the script will output the predictions
from the trained model, along with metadata about the architecture and model.
The trained model will be saved in the specified file path.

```sh
00:45:19 | ~/Documents/code/remote/coinbot
(.venv) git:(main | Δ) λ python -m coinbot.xor
2023-09-04 00:45:58,215 - INFO - dense.py:162 - Epoch 0, Loss: 0.9282104981979823
2023-09-04 00:45:58,241 - INFO - dense.py:162 - Epoch 1000, Loss: 0.007774923986908178
2023-09-04 00:45:58,245 - WARNING - dense.py:147 - Early stopping on epoch 1182, Loss: 0.002676929559403822
Running predictions:
[[0.00750384]
 [0.93021532]
 [0.93170549]
 [0.01551835]]
[{'type': 'Dense', 'input_dim': 2, 'output_dim': 2}, {'type': 'Tanh'}, {'type': 'Dense', 'input_dim': 2, 'output_dim': 1}, {'type': 'Tanh'}]
2023-09-04 00:45:58,247 - INFO - xor.py:89 - Saved model: models/coinbot-xor.h5
```

Remember that this script is tailored for the CoinBot XOR model and provides an
intuitive way to fine-tune training parameters and manage the model path using
command-line options.

### CoinBot Simulation for Pre-Training

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

    CoinBot: Automated Trading with Compound Interest
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

"""
CoinBot: Automated Trading with Compound Interest Strategy
Copyright (C) 2023  Austin Berrio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

coinbot/__init__.py

"Compound interest is the eighth wonder of the world. He who understands it, earns it... he who doesn't... pays it."
    - Albert Einstein
"""
import logging

__version__ = "0.0.2"
__name__ = "coinbot"
__agent__ = "teleprint-me/coinbot"
__source__ = "https://github.com/teleprint-me/coinbot"
__author__ = "Austin Berrio"
__email__ = "aberrio@teleprint.me"
__disclaimer__ = (
    "DISCLAIMER: I am a programmer and NOT an accredited financial expert. "
    "For important investment decisions, consult a certified financial professional. "
    "Do NOT rely on investment advice from anonymous sources online; always conduct thorough research."
)

# Set logging configuration
# NOTE: Can be overridden on a script-by-script basis
logging_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO)

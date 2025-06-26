"""
Copyright (C) 2023  Austin Berrio
@file coinbot.__init__
@brief Coinbot is a Python library for Automated Trading with Compound Interest Strategy.
@license AGPL
@ref https://en.wikipedia.org/wiki/Compound_interest

> Compound interest is the eighth wonder of the world.
> He who understands it, earns it... he who doesn't... pays it.
- Albert Einstein
"""

import logging

__version__ = "0.0.8"
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
logging.basicConfig(format=logging_format, level=logging.ERROR)

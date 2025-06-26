# CoinBot: AI-Powered Trading Model

**Automated Trading with a Compound Interest Strategy**

> ⚠️ **DISCLAIMER**
> I am a programmer, not a licensed financial advisor.
> Always consult a certified professional for investment decisions.
> Do **not** rely solely on anonymous sources or this software—conduct your own research.

## ⚠️ Active Development Notice

* 🛠️ This project is under **active development** and may change frequently.
* ⚠️ **Use at your own risk.**
* 🚨 **Always audit the output.**

## 📦 About

**CoinBot** is a modular framework for automated trading using averaging strategies:

* **Cost Averaging** — Buy fixed amounts at regular intervals.
* **Dynamic Cost Averaging** — Buy/sell/hold based on conditions around a fixed target.
* **Value Averaging** — Buy/sell/hold based on a moving dynamic target.

A future version will include a **time-series prediction model** based on GPT architecture in PyTorch. This will only be developed once the core interface is stable.

> For now, CoinBot only supports the **Coinbase Advanced Trade API** to keep the scope focused.
> Alpaca (for stock trading) may return later as a module if interest and resources allow.

## 🎯 Project Vision

This tool is a component of a larger effort to:

* Build a private treasury for long-term funding of open-source and experimental projects.
* Develop emotionless, strategy-driven models that operate consistently regardless of market sentiment.
* Integrate real-time and historical data to train models on trend-following, momentum, and mean-reversion patterns.
* Eventually output tax-ready documents such as **Form 8949 (CSV format)** for gains/loss tracking.

## 🚀 Quick Start

### Clone the Repository

```sh
git clone https://github.com/teleprint-me/coinbot coinbot
cd coinbot
```

### Setup Environment

```sh
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

> Optional (for model training, later):
>
> ```sh
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

## 🔐 Environment Variables

Create a `.env` file:

```sh
touch .env
vim .env
```

Add your keys:

```env
COINBASE_API_KEY='your-api-key'
COINBASE_API_SECRET='your-api-secret'
```

## ✅ Smoke Test

```sh
python -m coinbot.coinbase
```

## 📜 License

**CoinBot: Automated Trading with Compound Interest**
Copyright © 2023
Author: [Austin Berrio](https://teleprint.me)

Licensed under the **GNU Affero General Public License (AGPL)**:

* You are free to use, modify, and share under AGPL terms.
* Redistribution requires keeping this license.
* See [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/) for details.

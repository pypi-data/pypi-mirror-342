# cb-signalTUI

![Build](https://github.com/LoQiseaking69/Cb-signalTUI/actions/workflows/build.yml/badge.svg)

> A quant-grade, terminal-native crypto signal scanner with DEAP-powered optimization, Z-score fusion, and historical backtesting.

---

## 🚀 Features

- **🔍 Real-Time Cryptocurrency Scanning** — Parallel async fetches across 20+ pairs using aiohttp
- **📈 Advanced Technical Signal Fusion** — EMA spreads, Z-score, Savitzky-Golay slope, RSI, and volatility scoring
- **🧬 DEAP-based Z-threshold Optimization** — Learns optimal Z-score thresholds per asset in real-time
- **🧠 Strategy Classification** — Categorizes signals as `momentum`, `reversal`, or `neutral`
- **🖥️ Rich Terminal UI** — Color-coded TUI with auto-refresh and table output
- **🗣️ Voice Alerts** — pyttsx3-based text-to-speech for high-confidence signal calls
- **🧪 Backtesting** — Simulates signal accuracy, Sharpe ratio, and expectancy over future price lookahead
- **📂 SQLite Logging** — All signals stored with timestamp, price, z-score, strategy, and confidence
- **🔧 Modular Design** — Includes scanner, indicators, RL tuner, backtest logic, and environment config
- **🔁 Build Pipeline** — Auto-commits artifacts to `/built/`, publishes releases, and tags by version

---

## 🧱 Project Structure

```
cb-signalTUI/
├── cb_signal_tui/             # Main package directory
│   ├── __init__.py            # Version + API exports
│   ├── __main__.py            # Entry point CLI: scan or backtest
│   ├── scanner.py             # Async candle fetcher, signal emitter, DB logger
│   ├── indicators.py          # EMA, Z, RSI, slope, volatility logic
│   ├── ga_optimizer.py        # DEAP-powered genetic tuning
│   ├── backtest.py            # PnL, accuracy, Sharpe eval
│   ├── config.py              # ENV overrides and signal parameters
│   └── utils.py               # Alerting, logging, RSI, classification
│
├── .github/workflows/build.yml  # GitHub Actions CI/CD
├── pyproject.toml               # Build/packaging metadata
├── requirements.txt             # Dependencies
├── LICENSE                      # BSD-3-Clause License
├── README.md                    # This file
└── signals.db                   # SQLite runtime database (ignored by .git)
```

---

## 🛠️ Installation

```bash
git clone https://github.com/LoQiseaking69/Cb-signalTUI.git
cd Cb-signalTUI
pip install -r requirements.txt
```

To install from built artifacts:

```bash
pip install ./built/cb_signal_tui-*.whl
```

---

## 🚦 Usage

### Run the live scanner:
```bash
cb-signal-tui
```

### Run the backtester:
```bash
cb-signal-tui --backtest
```

To export results:
```bash
cb-signal-tui --backtest --export
```

---

## ⚙️ Configuration

Settings are located in `config.py` and respect ENV overrides:

- `PRODUCTS`: List of asset pairs
- `SETTINGS`: EMA spans and Z thresholds per asset
- `Z_SCORE_WINDOW`, `VOLATILITY_THRESHOLD`, `FLAT_SLOPE_THRESHOLD`: Signal tuning
- `STRATEGY_FILTER`: Types to allow in scanner (e.g., `momentum`, `reversal`)
- `ALERT_CONFIDENCE_THRESHOLD`: Alert trigger level
- `REFRESH_INTERVAL`: Terminal UI refresh rate
- `GRANULARITY`: Candle resolution (Coinbase granularity)

---

## 🧪 Backtesting

Evaluates signal outcome 20 minutes into the future:
```bash
cb-signal-tui --backtest
```

Outputs:
```
Backtest Accuracy: 83.45% | Sharpe: 1.823 | Expectancy: 0.0027 | Win Rate: 84.12%
```

---

## 🗄️ SQLite Signal Schema

```sql
CREATE TABLE signals (
    timestamp TEXT,
    asset TEXT,
    price REAL,
    z_score REAL,
    signal TEXT,
    confidence REAL,
    strategy TEXT
);
```

---

## 🖼️ Terminal Example

![img](https://github.com/LoQiseaking69/Cb-signalTUI/blob/main/IMG_1053.jpeg)

---

## 🤝 Contributing

1. Fork this repository
2. Create a branch: `git checkout -b feature-x`
3. Commit your changes
4. Open a PR

---

Built for precision. Tuned for performance. Stay ahead of the market.

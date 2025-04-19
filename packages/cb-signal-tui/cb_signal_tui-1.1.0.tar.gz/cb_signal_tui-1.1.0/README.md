# Cb-signalTUI

![Build](https://github.com/LoQiseaking69/Cb-signalTUI/actions/workflows/build.yml/badge.svg)

![img](https://github.com/LoQiseaking69/Cb-signalTUI/blob/main/8247439A-0E30-439A-AD1B-E41A16CC9891.png)

## Features

- **Real-Time Cryptocurrency Scanning**: Continuously scans a wide range of crypto pairs for trade signals.
- **Dynamic Technical Analysis**: Uses adaptive Exponential Moving Averages (EMA), Z-scores, slope detection, RSI, and volatility analysis.
- **Reinforcement Learning Optimization**: Dynamically tunes Z-score thresholds using DEAP-based RL algorithms.
- **Strategy Classification**: Differentiates between momentum, reversal, and neutral strategies.
- **Live Terminal UI**: Displays results in a color-coded, real-time TUI with `rich.live`.
- **Asynchronous Data Fetching**: Utilizes `aiohttp` and retries on failure for reliable data streaming.
- **Voice Alerts**: Uses `pyttsx3` for real-time vocal alerts when high-confidence signals occur.
- **Database Logging**: Stores all signal events with `aiosqlite` for historical reference.
- **Backtesting Accuracy**: Includes a backtesting module to evaluate signal performance.
- **Custom Configs per Asset**: Each asset has its own EMA and Z-score threshold settings.
- **Auto-Build Artifacts**: Built packages are committed to `/built/` on each push to `main`.

## Project Structure

```
Cb-signalTUI/
├── cb_signal_tui/             # Main package directory
│   ├── __init__.py
│   └── __main__.py            # Entry point with config
├── built/                     # Auto-committed build artifacts (.whl, .tar.gz)
│   └── cb_signal_tui-*.whl
├── dist/                      # Local build output (ignored by .git)
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions workflow
├── requirements.txt           # Dependencies
├── pyproject.toml             # Build system config
├── README.md                  # Project documentation
└── signals.db                 # SQLite DB (optional, runtime-generated)
```

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/LoQiseaking69/Cb-signalTUI.git
   cd Cb-signalTUI
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Export a shortcut path to the `.whl` package for faster installs:

   ```bash
   echo 'export cb_sigTUI="$HOME/Desktop/Cb-signalTUI-main/built/*.whl"' >> ~/.bashrc
   source ~/.bashrc
   ```

   Now you can install with:

   ```bash
   pip install $cb_sigTUI
   ```

## Dependencies

```
aiohttp
aiosqlite
pandas
numpy
pyttsx3
rich
scipy
deap
tabulate
```

## Usage

Run the scanner:

```bash
cb-signal-tui
```

### Example Output

![img](https://github.com/LoQiseaking69/Cb-signalTUI/blob/main/IMG_1053.jpeg)

## Configuration

Edit settings in `cb_signal_tui/__main__.py`:

- `PRODUCTS`: Assets to scan (`BTC-USD`, `ETH-USD`, etc.)
- `SETTINGS`: EMA periods and Z-score threshold settings per asset
- `Z_SCORE_WINDOW`, `VOLATILITY_THRESHOLD`, `FLAT_SLOPE_THRESHOLD`: Signal tuning
- `STRATEGY_FILTER`: Control which strategies trigger alerts (`momentum`, `reversal`)
- `ALERT_CONFIDENCE_THRESHOLD`: Minimum confidence for triggering an alert
- `REFRESH_INTERVAL`: Refresh rate for terminal UI
- `GRANULARITY`: Time granularity for fetched data (in seconds)

## Database

SQLite database (`signals.db`) schema:

```sql
CREATE TABLE IF NOT EXISTS signals (
    timestamp TEXT,
    asset TEXT,
    price REAL,
    z_score REAL,
    signal TEXT,
    confidence REAL,
    strategy TEXT
);
```

## Backtesting

Run the backtesting module to evaluate signal accuracy:

```bash
cb-signal-tui-backtest
```

The backtest fetches historical data and compares signal predictions with actual price movements.

## Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b my-feature`).
3. Make your changes.
4. Push and open a Pull Request.

---

Built for precision. Tuned for performance. Stay ahead of the market.

"""
cb_signal_tui
=============

A high-performance, terminal-native crypto signal scanner for Coinbase markets.
This system integrates Z-score anomaly detection, EMA momentum analysis, RSI filtering,
trend slope estimation via Savitzky-Golay filtering, and adaptive volatility-aware logic —
optimized in real-time using DEAP-based reinforcement learning — to surface high-confidence
BUY/SELL signals for a broad set of digital assets.

Core Features:
--------------
- Strategy fusion: Z-score, EMA differentials, RSI, Savitzky-Golay slope, volatility scoring
- Online reinforcement learning (DEAP) for dynamic Z-score threshold tuning per asset
- Strategy classification (momentum/reversal) based on slope sensitivity
- Confidence scoring scaled by Z-score deviation, slope integrity, and volatility
- Signal cooldown mechanism to avoid redundant signals within time windows
- Live terminal dashboard via Rich with auto-refreshing, color-coded signal table
- Real-time speech alerts using pyttsx3 for actionable BUY/SELL signals
- Fully asynchronous architecture (aiohttp + aiosqlite) with zero blocking
- Persistent SQLite logging of all signal metadata (`signals.db`)
- Fault-tolerant data fetching with retries and exponential backoff
- CLI-accessible asynchronous backtesting system with accuracy breakdown
- Tabbable terminal output of results using tabulate (fancy_grid style)
- CLI-based control: `--backtest` flag for standalone evaluation mode
- Graceful shutdown support on keyboard interrupts

Exposes:
--------
- main():         Starts the live signal scanner loop
- cli():          CLI dispatcher supporting --backtest execution
- run_backtest(): Asynchronously evaluates past signals vs real market outcome
- SETTINGS:       Asset-specific EMA spans and adaptive Z-score thresholds

"""

from .__main__ import main, cli, run_backtest, SETTINGS

__version__ = "1.2.2"
__author__ = "LoQiseaking69"

"""
cb_signal_tui
=============

A high-performance, terminal-native crypto signal scanner for Coinbase markets.
This system integrates Z-score anomaly detection, EMA momentum analysis, trend slope
evaluation using Savitzky-Golay filtering, and adaptive volatility calibration — optimized
by DEAP-based reinforcement learning — to surface high-confidence BUY/SELL signals.

Core Features:
--------------
- Strategy fusion: Z-score, EMA differentials, RSI, volatility, Savitzky-Golay slope
- Reinforcement learning (DEAP) for adaptive Z-score threshold tuning per asset
- Momentum and reversal classification via trend/slope analysis
- Dynamic confidence scoring based on volatility and recent Z-score consistency
- Live terminal dashboard with Rich (auto-refreshing, color-coded signal board)
- Real-time speech alerts via pyttsx3 for BUY/SELL triggers
- Fully async architecture using aiohttp + aiosqlite for non-blocking ops
- Persistent logging of all signals to a local SQLite DB (`signals.db`)
- Fault-tolerant fetch logic with retries and exponential backoff
- Built-in asynchronous backtester for signal accuracy validation
- Tabbable output of backtest results via tabulate
- Graceful shutdown handling and CLI launch mode

Exposes:
--------
- main():         Launches real-time signal scanner (async loop)
- cli():          CLI entry point, runs scanner and backtester
- run_backtest(): Performs async historical evaluation of generated signals
- SETTINGS:       Config dict containing asset-specific EMA/z_thresh tuning

"""

from .__main__ import main, cli, run_backtest, SETTINGS

__version__ = "1.1.0"
__author__ = "LoQiseaking69"

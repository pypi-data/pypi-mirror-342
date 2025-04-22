"""
cb_signal_tui
=============

A quant-grade, terminal-native crypto signal scanner for Coinbase markets.

Key Features:
-------------
- Strategy fusion: Z-score, EMA spread, RSI, Savitzky-Golay slope, volatility amplification
- Real-time signal generation with adaptive Z-threshold via DEAP genetic algorithms
- Signal classification (momentum / reversal) with volatility-adjusted confidence scoring
- Asynchronous architecture using aiohttp + aiosqlite for fast parallel scanning and logging
- Live Rich terminal dashboard with TTS alerts for actionable signals
- CLI backtesting with Sharpe Ratio, PnL, expectancy, and CSV export
- Modular configuration with ENV override support and per-asset strategy tuning

Public Exports:
---------------
- cli():             CLI entrypoint (live scan / backtest)
- main():            Scanner loop coroutine
- run_backtest():    Async backtest evaluator
- SETTINGS:          Per-asset strategy map
"""

from .__main__ import cli, run_scanner as main
from .backtest import run_backtest
from .config import SETTINGS

__version__ = "1.4.0"
__author__ = "LoQiseaking69"
__license__ = "BSD-3-Clause"
__copyright__ = "Copyright (c) 2025 LoQiseaking69"
__description__ = "A quant-grade, terminal-native crypto signal scanner for Coinbase markets."
__all__ = ["cli", "main", "run_backtest", "SETTINGS"]

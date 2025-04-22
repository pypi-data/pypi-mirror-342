"""
config.py — Central configuration module for cb_signal_tui
Supports ENV overrides and is typed for safety
"""

import os
from typing import Dict, Tuple, Union

# === Strategy & Signal Tuning ===
STRATEGY_FILTER = {"momentum", "reversal"}
ALERT_CONFIDENCE_THRESHOLD: float = float(os.getenv("ALERT_CONFIDENCE_THRESHOLD", 0.8))
REFRESH_INTERVAL: int = int(os.getenv("REFRESH_INTERVAL", 10))
Z_SCORE_WINDOW: int = int(os.getenv("Z_SCORE_WINDOW", 20))
VOLATILITY_THRESHOLD: float = float(os.getenv("VOLATILITY_THRESHOLD", 0.015))
FLAT_SLOPE_THRESHOLD: float = float(os.getenv("FLAT_SLOPE_THRESHOLD", 1e-4))

# === API & Data Feed ===
GRANULARITY: int = int(os.getenv("GRANULARITY", 300))
RETRY_LIMIT: int = int(os.getenv("RETRY_LIMIT", 3))
API_URL: str = os.getenv("API_URL", "https://api.exchange.coinbase.com/products/{}/candles")

# === Database ===
DB_PATH: str = os.getenv("DB_PATH", "signals.db")

# === RL Optimization ===
GA_POP_SIZE: int = int(os.getenv("GA_POP_SIZE", 10))
GA_NUM_GEN: int = int(os.getenv("GA_NUM_GEN", 5))
GA_MUT_SIGMA: float = float(os.getenv("GA_MUT_SIGMA", 0.2))
GA_SEED: int = int(os.getenv("GA_SEED", 42))

# === Per-Asset Configuration ===
SETTINGS: Dict[str, Dict[str, Union[Tuple[int, int], float]]] = {
    "BTC-USD":   {"ema": (12, 26), "z_thresh": 1.5},
    "ETH-USD":   {"ema": (10, 21), "z_thresh": 1.4},
    "SOL-USD":   {"ema": (10, 21), "z_thresh": 1.6},
    "ADA-USD":   {"ema": (8, 19),  "z_thresh": 1.3},
    "AVAX-USD":  {"ema": (9, 18),  "z_thresh": 1.4},
    "DOGE-USD":  {"ema": (7, 17),  "z_thresh": 1.2},
    "SHIB-USD":  {"ema": (6, 15),  "z_thresh": 1.1},
    "XRP-USD":   {"ema": (9, 20),  "z_thresh": 1.4},
    "LINK-USD":  {"ema": (9, 20),  "z_thresh": 1.5},
    "MATIC-USD": {"ema": (8, 19),  "z_thresh": 1.3},
    "ARB-USD":   {"ema": (7, 18),  "z_thresh": 1.3},
    "OP-USD":    {"ema": (8, 19),  "z_thresh": 1.4},
    "APT-USD":   {"ema": (9, 21),  "z_thresh": 1.5},
    "INJ-USD":   {"ema": (10, 22), "z_thresh": 1.6},
    "RNDR-USD":  {"ema": (9, 20),  "z_thresh": 1.4},
    "TIA-USD":   {"ema": (8, 19),  "z_thresh": 1.4},
    "PEPE-USD":  {"ema": (6, 15),  "z_thresh": 1.2},
    "FET-USD":   {"ema": (9, 21),  "z_thresh": 1.5},
    "JTO-USD":   {"ema": (8, 20),  "z_thresh": 1.4},
    "WIF-USD":   {"ema": (7, 17),  "z_thresh": 1.3},
}

# === Asset List Auto-Generated ===
PRODUCTS = list(SETTINGS)
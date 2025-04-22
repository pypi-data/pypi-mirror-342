"""
indicators.py — Core indicator calculation using EMA, RSI, Z-Score, slope and classification
"""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from typing import Tuple, Union

from cb_signal_tui.config import SETTINGS, Z_SCORE_WINDOW, FLAT_SLOPE_THRESHOLD, VOLATILITY_THRESHOLD
from cb_signal_tui.utils import calculate_rsi, classify_strategy
from cb_signal_tui.ga_optimizer import optimize_threshold

def calculate_indicators(df: pd.DataFrame, product: str) -> Tuple[str, float, float, float, str]:
    if df is None or "close" not in df or len(df) < Z_SCORE_WINDOW + 10:
        return "HOLD", np.nan, np.nan, 0.0, "neutral"

    short, long = SETTINGS[product]["ema"]
    z_thresh = optimize_threshold(df, product)
    SETTINGS[product]["z_thresh"] = z_thresh  # Real-time update

    close = df["close"]
    ema_diff = close.ewm(span=short).mean() - close.ewm(span=long).mean()

    z_scores = ((ema_diff - ema_diff.rolling(Z_SCORE_WINDOW).mean()) /
                ema_diff.rolling(Z_SCORE_WINDOW).std(ddof=0).replace(0, 1e-8)).fillna(0).replace([np.inf, -np.inf], 0)

    # Key signals
    latest_price = float(close.iloc[-1])
    latest_z = float(z_scores.iloc[-1])
    slope = float(np.polyfit(range(Z_SCORE_WINDOW), savgol_filter(close[-Z_SCORE_WINDOW:], 5, 2), 1)[0])
    rsi = float(calculate_rsi(close).iloc[-1])
    volatility = float(close.pct_change().rolling(Z_SCORE_WINDOW).std().iloc[-1])
    confirm = sum((abs(z_scores.iloc[-i]) > z_thresh) for i in range(1, 4))

    # Decision Logic
    signal, confidence = "HOLD", 0.0
    if latest_z > z_thresh and rsi < 70 and confirm >= 2 and slope >= FLAT_SLOPE_THRESHOLD:
        signal = "BUY"
        confidence = min((latest_z - z_thresh) / 2, 1.0)
    elif latest_z < -z_thresh and rsi > 30 and confirm >= 2 and slope <= -FLAT_SLOPE_THRESHOLD:
        signal = "SELL"
        confidence = min((-latest_z - z_thresh) / 2, 1.0)

    # Volatility Amplification
    if signal != "HOLD" and volatility > VOLATILITY_THRESHOLD:
        confidence = min(confidence * 1.2, 1.0)

    # Flat slope penalty
    if abs(slope) < FLAT_SLOPE_THRESHOLD:
        confidence *= 0.25
        signal = "HOLD"

    strategy = classify_strategy(latest_z, slope)
    return signal, latest_price, latest_z, confidence, strategy

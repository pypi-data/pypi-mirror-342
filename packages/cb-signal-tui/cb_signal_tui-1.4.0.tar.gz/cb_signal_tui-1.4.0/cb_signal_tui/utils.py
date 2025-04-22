"""
utils.py — General-purpose utilities: alerting, classification, logging, risk scoring
"""

import pyttsx3
import pandas as pd
import numpy as np
import logging
from cb_signal_tui.config import FLAT_SLOPE_THRESHOLD

logger = logging.getLogger("cb_signal_tui")

# === TTS Alerting ===
def speak_alert(msg: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.8)
        engine.say(msg)
        engine.runAndWait()
    except Exception as e:
        logger.warning(f"[TTS Error] {e}")

# === RSI Calculation ===
def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss.replace(0, 1e-8)
    return 100 - (100 / (1 + rs))

# === Strategy Classification ===
def classify_strategy(z: float, slope: float) -> str:
    if abs(z) > 2.0 and abs(slope) > FLAT_SLOPE_THRESHOLD:
        return "momentum"
    elif abs(z) > 1.5 and abs(slope) <= FLAT_SLOPE_THRESHOLD:
        return "reversal"
    return "neutral"

# === Risk-Weighted Confidence Score (optional use) ===
def score_risk_weighted(confidence: float, volatility: float) -> float:
    if volatility <= 0:
        return 0.0
    return round(confidence / (volatility + 1e-6), 4)

# === Logging Setup ===
def init_logger(name: str = "cb_signal_tui", level=logging.INFO) -> logging.Logger:
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    if not log.handlers:
        log.addHandler(handler)
    return log
"""
scanner.py — Signal scanning logic, candle fetcher, DB recording, and Rich table builder
"""

import asyncio
import aiohttp
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Union
import aiosqlite
import logging
from rich.console import Console
from rich.table import Table

from cb_signal_tui.config import (
    API_URL, RETRY_LIMIT, PRODUCTS, DB_PATH,
    STRATEGY_FILTER, ALERT_CONFIDENCE_THRESHOLD
)
from cb_signal_tui.indicators import calculate_indicators
from cb_signal_tui.utils import speak_alert

logger = logging.getLogger("cb_signal_tui")
console = Console()

# === Candle Fetching ===
async def fetch_candles(session: aiohttp.ClientSession, product_id: str, granularity: int = 300) -> Union[pd.DataFrame, None]:
    url = API_URL.format(product_id)
    params = {'granularity': granularity}

    for attempt in range(RETRY_LIMIT):
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if isinstance(data, dict):
                    raise ValueError(data.get("message", "Invalid response"))

                df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
                df["time"] = pd.to_datetime(df["time"], unit="s")
                return df.sort_values("time").reset_index(drop=True)
        except Exception as e:
            logger.warning(f"[{product_id}] Fetch retry {attempt+1}: {e}")
            await asyncio.sleep(min(2 ** attempt * 0.2, 2.0))
    return None

# === Product Scan Logic ===
async def scan_product(session, product: str, db_conn: aiosqlite.Connection):
    df = await fetch_candles(session, product)
    if df is None:
        return None

    signal, price, z_score, conf, strategy = await asyncio.to_thread(calculate_indicators, df, product)
    if np.isnan(price) or strategy not in STRATEGY_FILTER or signal == "HOLD":
        return None

    # Cooldown check
    async with db_conn.execute(
        "SELECT timestamp FROM signals WHERE asset = ? AND signal = ? ORDER BY timestamp DESC LIMIT 1",
        (product, signal)
    ) as cursor:
        recent = await cursor.fetchone()
    if recent:
        last_time = datetime.fromisoformat(recent[0])
        if datetime.utcnow() - last_time < timedelta(minutes=3):
            logger.debug(f"[{product}] Signal throttled (cooldown)")
            return None

    timestamp = datetime.utcnow().isoformat()
    await db_conn.execute(
        "INSERT INTO signals VALUES (?, ?, ?, ?, ?, ?, ?)",
        (timestamp, product, price, z_score, signal, conf, strategy)
    )
    await db_conn.commit()

    # Trigger visual and voice alert
    if conf >= ALERT_CONFIDENCE_THRESHOLD:
        msg = f"{signal} signal for {product}. Confidence {conf:.0%}"
        console.print(f"[bold {'green' if signal == 'BUY' else 'red'} blink]{msg}[/]")
        speak_alert(msg)

    price_fmt = f"${price:,.6f}" if price < 1 else f"${price:,.2f}"
    return signal, conf, (
        f"[bold]{product}[/bold]",
        f"[white]{price_fmt}[/white]",
        f"[cyan]{z_score:.2f}[/cyan]",
        f"[{'green' if signal == 'BUY' else 'red'}]{signal}[/{'green' if signal == 'BUY' else 'red'}]",
        f"[bold]{conf:.2%}[/bold]"
    )

# === Table Builder ===
def build_table(results):
    table = Table(title=f"📡 Crypto Signals @ {datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC")
    table.add_column("Asset")
    table.add_column("Price", justify="right")
    table.add_column("Z-Score", justify="center")
    table.add_column("Signal", justify="center")
    table.add_column("Confidence", justify="right")
    for _, _, (asset, price, z, signal, conf) in sorted(filter(None, results), key=lambda x: (x[0] == 'HOLD', -x[1])):
        table.add_row(asset, price, z, signal, conf)
    return table
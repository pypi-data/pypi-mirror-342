"""
backtest.py — Historical signal evaluation with accuracy, PnL, Sharpe Ratio, and CSV export
"""

import aiohttp
import aiosqlite
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tabulate import tabulate
from cb_signal_tui.config import DB_PATH, API_URL, GRANULARITY
from rich.console import Console
import logging
import os

logger = logging.getLogger("cb_signal_tui")
console = Console()

# === Fetch Future Price by Time ===
async def fetch_price_at(product_id: str, target_time: datetime) -> float:
    url = API_URL.format(product_id)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"granularity": GRANULARITY}) as resp:
                data = await resp.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    future = df[df['time'] >= target_time].head(1)
                    if not future.empty:
                        return float(future['close'].iloc[0])
    except Exception as e:
        logger.error(f"[{product_id}] Backtest fetch error: {e}")
    return np.nan

# === Full Accuracy Run ===
async def run_backtest(export_csv: bool = False):
    console.print("\n[bold magenta]Running Backtest Evaluation...[/bold magenta]")

    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT * FROM signals WHERE signal IN ('BUY', 'SELL')")
        rows = await cursor.fetchall()

    if not rows:
        console.print("[yellow]No signals to backtest.[/yellow]")
        return

    df = pd.DataFrame(rows, columns=["timestamp", "asset", "price", "z_score", "signal", "confidence", "strategy"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    results = []
    profits = []

    for _, row in df.iterrows():
        future_time = row["timestamp"] + timedelta(minutes=20)
        future_price = await fetch_price_at(row["asset"], future_time)
        if np.isnan(future_price):
            continue

        price_then = row["price"]
        pnl = future_price - price_then if row["signal"] == "BUY" else price_then - future_price
        correct = pnl > 0
        profits.append(pnl)

        results.append({
            "Asset": row["asset"],
            "Signal Time": row["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            "Signal": row["signal"],
            "Price Then": round(price_then, 4),
            "Price Later": round(future_price, 4),
            "Correct": "✅" if correct else "❌",
            "PnL": round(pnl, 6)
        })

    result_df = pd.DataFrame(results)
    accuracy = result_df["Correct"].apply(lambda x: x == "✅").mean()
    sharpe_ratio = (
        np.mean(profits) / (np.std(profits) + 1e-8) * np.sqrt(len(profits))
        if profits else 0.0
    )
    expectancy = np.mean(profits) if profits else 0.0
    win_rate = result_df["Correct"].value_counts(normalize=True).get("✅", 0.0)

    console.print(f"\n[green]Backtest Accuracy: {accuracy:.2%} | Sharpe: {sharpe_ratio:.3f} | Expectancy: {expectancy:.4f} | Win Rate: {win_rate:.2%}[/green]\n")
    print(tabulate(result_df, headers="keys", tablefmt="fancy_grid"))

    if export_csv:
        path = f"backtest_results_{datetime.utcnow():%Y%m%d%H%M%S}.csv"
        result_df.to_csv(path, index=False)
        console.print(f"[cyan]Exported: {path}[/cyan]")
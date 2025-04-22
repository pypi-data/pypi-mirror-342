"""
__main__.py — Entrypoint for cb_signal_tui
Supports: live scan mode, backtest mode, CLI routing
"""

import sys
import asyncio
import aiohttp
import aiosqlite
from rich.live import Live
from rich.console import Console
import logging

from cb_signal_tui.config import DB_PATH, PRODUCTS, REFRESH_INTERVAL
from cb_signal_tui.scanner import scan_product, build_table
from cb_signal_tui.backtest import run_backtest
from cb_signal_tui.utils import init_logger

logger = init_logger()
console = Console()

# === Live Scanner Runtime ===
async def run_scanner():
    async with aiosqlite.connect(DB_PATH) as db_conn:
        await db_conn.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                timestamp TEXT, asset TEXT, price REAL, z_score REAL,
                signal TEXT, confidence REAL, strategy TEXT
            )""")
        await db_conn.commit()

        async with aiohttp.ClientSession() as session:
            with Live(console=console, refresh_per_second=2):
                while True:
                    try:
                        results = await asyncio.gather(*(scan_product(session, p, db_conn) for p in PRODUCTS))
                        table = build_table(results)
                        console.clear()
                        console.print(table)
                        await asyncio.sleep(REFRESH_INTERVAL)
                    except Exception as e:
                        logger.exception(f"[Runtime Error] {e}")

# === CLI Dispatcher ===
def cli():
    try:
        if "--backtest" in sys.argv:
            asyncio.run(run_backtest(export_csv="--export" in sys.argv))
        else:
            asyncio.run(run_scanner())
    except KeyboardInterrupt:
        console.print("\n[bold red]Scanner stopped by user.[/bold red]")
    except Exception as e:
        logger.exception(f"[CLI Error] {e}")

# === Python Module Entrypoint ===
if __name__ == '__main__':
    cli()

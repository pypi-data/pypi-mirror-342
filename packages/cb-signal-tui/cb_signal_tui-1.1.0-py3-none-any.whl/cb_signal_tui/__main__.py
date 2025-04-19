# === Imports ===
import asyncio, aiohttp, aiosqlite, pyttsx3, logging
import pandas as pd, numpy as np
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.live import Live
from scipy.signal import savgol_filter
from typing import Optional, Tuple, Dict, Any, List
from deap import base, creator, tools, algorithms
from tabulate import tabulate

# === Configuration ===
STRATEGY_FILTER = {"momentum", "reversal"}
ALERT_CONFIDENCE_THRESHOLD = 0.8
REFRESH_INTERVAL = 10
GRANULARITY = 300
Z_SCORE_WINDOW = 20
VOLATILITY_THRESHOLD = 0.015
FLAT_SLOPE_THRESHOLD = 1e-4
API_URL = "https://api.exchange.coinbase.com/products/{}/candles"
RETRY_LIMIT = 3
DB_PATH = "signals.db"

SETTINGS: Dict[str, Dict[str, Any]] = {
    'BTC-USD': {'ema': (12, 26), 'z_thresh': 1.5}, 'ETH-USD': {'ema': (10, 21), 'z_thresh': 1.4},
    'SOL-USD': {'ema': (10, 21), 'z_thresh': 1.6}, 'ADA-USD': {'ema': (8, 19), 'z_thresh': 1.3},
    'AVAX-USD': {'ema': (9, 18), 'z_thresh': 1.4}, 'DOGE-USD': {'ema': (7, 17), 'z_thresh': 1.2},
    'SHIB-USD': {'ema': (6, 15), 'z_thresh': 1.1}, 'XRP-USD': {'ema': (9, 20), 'z_thresh': 1.4},
    'LINK-USD': {'ema': (9, 20), 'z_thresh': 1.5}, 'MATIC-USD': {'ema': (8, 19), 'z_thresh': 1.3},
    'ARB-USD': {'ema': (7, 18), 'z_thresh': 1.3}, 'OP-USD': {'ema': (8, 19), 'z_thresh': 1.4},
    'APT-USD': {'ema': (9, 21), 'z_thresh': 1.5}, 'INJ-USD': {'ema': (10, 22), 'z_thresh': 1.6},
    'RNDR-USD': {'ema': (9, 20), 'z_thresh': 1.4}, 'TIA-USD': {'ema': (8, 19), 'z_thresh': 1.4},
    'PEPE-USD': {'ema': (6, 15), 'z_thresh': 1.2}, 'FET-USD': {'ema': (9, 21), 'z_thresh': 1.5},
    'JTO-USD': {'ema': (8, 20), 'z_thresh': 1.4}, 'WIF-USD': {'ema': (7, 17), 'z_thresh': 1.3}
}
PRODUCTS = list(SETTINGS.keys())

# === Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
console = Console()

# === Utils ===
def speak_alert(msg: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        engine.say(msg)
        engine.runAndWait()
    except Exception as e:
        logger.warning(f"TTS error: {e}")

def calculate_rsi(series: pd.Series, period=14) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss.replace(0, 1e-8)
    return 100 - (100 / (1 + rs))

def classify_strategy(z: float, slope: float) -> str:
    if abs(z) > 2.0 and abs(slope) > FLAT_SLOPE_THRESHOLD: return "momentum"
    elif abs(z) > 1.5 and abs(slope) <= FLAT_SLOPE_THRESHOLD: return "reversal"
    return "neutral"

# === RL Optimizer ===
def evaluate_strategy_rl(df: pd.DataFrame, product: str):
    if len(df) < 40: return SETTINGS[product]['z_thresh']

    def fitness(individual):
        z_thresh = individual[0]
        close = df['close']
        short, long = SETTINGS[product]['ema']
        delta = close.ewm(span=short).mean() - close.ewm(span=long).mean()
        z = ((delta - delta.rolling(Z_SCORE_WINDOW).mean()) /
             delta.rolling(Z_SCORE_WINDOW).std(ddof=0).replace(0, 1e-8)).fillna(0)
        score = 0
        for i in range(5, len(z) - 1):
            if z[i] > z_thresh:
                score += close[i + 1] - close[i]
            elif z[i] < -z_thresh:
                score += close[i] - close[i + 1]
        return score,

    # Avoid duplicate class error
    if "FitnessMax" not in creator.__dict__:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if "Individual" not in creator.__dict__:
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", lambda: np.random.uniform(1.0, 3.0))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=10)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=5, verbose=False)
    best = tools.selBest(pop, k=1)[0]
    return round(best[0], 3)

# === Indicator Computation ===
def calculate_indicators(df: pd.DataFrame, product: str):
    short, long = SETTINGS[product]['ema']
    z_thresh = evaluate_strategy_rl(df, product)

    if df is None or len(df) < long + Z_SCORE_WINDOW + 10:
        return 'HOLD', np.nan, np.nan, 0.0, "neutral"

    close = df['close']
    delta = close.ewm(span=short).mean() - close.ewm(span=long).mean()
    z_scores = ((delta - delta.rolling(Z_SCORE_WINDOW).mean()) /
                delta.rolling(Z_SCORE_WINDOW).std(ddof=0).replace(0, 1e-8)).replace([np.inf, -np.inf], 0).fillna(0)

    latest_price = float(close.iloc[-1])
    latest_z = float(z_scores.iloc[-1])
    slope = float(np.polyfit(range(Z_SCORE_WINDOW), savgol_filter(close[-Z_SCORE_WINDOW:], 5, 2), 1)[0])
    rsi = calculate_rsi(close).iloc[-1]
    volatility = float(close.pct_change().rolling(Z_SCORE_WINDOW).std().iloc[-1])
    confirm = sum((abs(z_scores.iloc[-i]) > z_thresh) for i in range(1, 4))

    signal, confidence = 'HOLD', 0.0
    if latest_z > z_thresh and rsi < 70 and confirm >= 2:
        signal, confidence = 'BUY', min((latest_z - z_thresh) / 2, 1.0)
    elif latest_z < -z_thresh and rsi > 30 and confirm >= 2:
        signal, confidence = 'SELL', min((-latest_z - z_thresh) / 2, 1.0)

    if signal != 'HOLD' and volatility > VOLATILITY_THRESHOLD:
        confidence = min(confidence * 1.2, 1.0)
    if abs(slope) < FLAT_SLOPE_THRESHOLD:
        signal, confidence = 'HOLD', confidence * 0.25

    strategy = classify_strategy(latest_z, slope)
    return signal, latest_price, latest_z, confidence, strategy

# === Async Scan + Table ===
async def fetch_candles(session: aiohttp.ClientSession, product_id: str):
    url, params = API_URL.format(product_id), {'granularity': GRANULARITY}
    for attempt in range(RETRY_LIMIT):
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if isinstance(data, dict): raise ValueError(data.get("message", "Invalid response"))
                df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df.sort_values('time').reset_index(drop=True)
        except Exception as e:
            await asyncio.sleep(min(2 ** attempt * 0.2, 2.0))
    return None

async def scan_product(session, product, db_conn):
    df = await fetch_candles(session, product)
    if df is None: return None

    signal, price, z_score, conf, strategy = await asyncio.to_thread(calculate_indicators, df, product)
    if np.isnan(price) or strategy not in STRATEGY_FILTER: return None

    timestamp = datetime.utcnow().isoformat()
    await db_conn.execute("INSERT INTO signals VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (timestamp, product, price, z_score, signal, conf, strategy))
    await db_conn.commit()

    if signal in {"BUY", "SELL"} and conf >= ALERT_CONFIDENCE_THRESHOLD:
        msg = f"{signal.capitalize()} signal for {product}. Confidence {conf:.0%}"
        console.print(f"[bold {'green' if signal == 'BUY' else 'red'} blink]{msg}[/]")
        speak_alert(msg)

    price_fmt = f"${price:,.6f}" if price < 1 else f"${price:,.2f}"
    return signal, conf, (
        f"[bold]{product}[/bold]",
        f"[white]{price_fmt}[/white]",
        f"[cyan]{z_score:.2f}[/cyan]",
        f"[{'green' if signal == 'BUY' else 'red' if signal == 'SELL' else 'yellow'}]{signal}[/{'green' if signal == 'BUY' else 'red' if signal == 'SELL' else 'yellow'}]",
        f"[bold]{conf:.2%}[/bold]"
    )

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

# === Backtest Accuracy ===
async def fetch_price_at(product_id: str, target_time: datetime):
    url = API_URL.format(product_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"granularity": GRANULARITY}) as resp:
            try:
                data = await resp.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    future = df[df['time'] >= target_time].head(1)
                    if not future.empty:
                        return float(future['close'].iloc[0])
            except Exception as e:
                logger.error(f"Backtest fetch error: {e}")
    return None

async def run_backtest():
    console.print("\n[bold magenta]Running Backtest...[/bold magenta]")
    conn = await aiosqlite.connect(DB_PATH)
    cursor = await conn.execute("SELECT * FROM signals WHERE signal IN ('BUY', 'SELL')")
    rows = await cursor.fetchall()
    await conn.close()
    if not rows:
        console.print("[yellow]No signals to backtest.[/yellow]")
        return

    df = pd.DataFrame(rows, columns=["timestamp", "asset", "price", "z_score", "signal", "confidence", "strategy"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    results = []

    for _, row in df.iterrows():
        future_time = row["timestamp"] + timedelta(minutes=20)
        price_later = await fetch_price_at(row["asset"], future_time)
        if price_later is not None:
            correct = ((row["signal"] == "BUY" and price_later > row["price"]) or
                       (row["signal"] == "SELL" and price_later < row["price"]))
            results.append({
                "Asset": row["asset"], "Signal Time": row["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "Signal": row["signal"], "Price Then": round(row["price"], 4),
                "Price Later": round(price_later, 4), "Correct": "✅" if correct else "❌"
            })

    df_result = pd.DataFrame(results)
    acc = df_result["Correct"].apply(lambda x: x == "✅").mean() if not df_result.empty else 0.0
    console.print(f"\n[green]Backtest Accuracy: {acc:.2%}[/green]")
    print(tabulate(df_result, headers="keys", tablefmt="fancy_grid"))

# === Runner ===
async def run_scanner():
    async with aiosqlite.connect(DB_PATH) as db_conn:
        await db_conn.execute("""CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT, asset TEXT, price REAL, z_score REAL,
            signal TEXT, confidence REAL, strategy TEXT)""")
        await db_conn.commit()

        async with aiohttp.ClientSession() as session:
            with Live(console=console, refresh_per_second=2):
                while True:
                    results = await asyncio.gather(*(scan_product(session, p, db_conn) for p in PRODUCTS))
                    table = build_table(results)
                    console.clear()
                    console.print(table)
                    await asyncio.sleep(REFRESH_INTERVAL)

async def main():
    try:
        await run_scanner()
    except KeyboardInterrupt:
        console.print("\n[bold red]Scanner stopped by user.[/bold red]")

def cli():
    asyncio.run(main())
    asyncio.run(run_backtest())

# === Entrypoint ===
if __name__ == '__main__':
    cli()

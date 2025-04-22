"""
ga_optimizer.py — Genetic Algorithm threshold optimizer using DEAP
"""

import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
from cb_signal_tui.config import (
    SETTINGS, Z_SCORE_WINDOW,
    GA_POP_SIZE, GA_NUM_GEN, GA_MUT_SIGMA, GA_SEED
)

def optimize_threshold(df: pd.DataFrame, product: str) -> float:
    if df is None or len(df) < Z_SCORE_WINDOW + 10:
        return SETTINGS[product]["z_thresh"]

    close = df["close"]
    short, long = SETTINGS[product]["ema"]
    delta = close.ewm(span=short).mean() - close.ewm(span=long).mean()
    z_series = ((delta - delta.rolling(Z_SCORE_WINDOW).mean()) /
                delta.rolling(Z_SCORE_WINDOW).std(ddof=0).replace(0, 1e-8)).fillna(0)

    def fitness(individual):
        z_thresh = individual[0]
        score = 0.0
        for i in range(5, len(z_series) - 1):
            if z_series[i] > z_thresh:
                score += close[i + 1] - close[i]
            elif z_series[i] < -z_thresh:
                score += close[i] - close[i + 1]
        return score,

    if "FitnessMax" not in creator.__dict__:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if "Individual" not in creator.__dict__:
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    np.random.seed(GA_SEED)
    toolbox.register("attr_float", lambda: np.random.uniform(1.0, 3.0))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=GA_MUT_SIGMA, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=GA_POP_SIZE)
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.3, ngen=GA_NUM_GEN, verbose=False)
    best = tools.selBest(population, k=1)[0]
    return round(best[0], 3)
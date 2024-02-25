import pandas as pd
from set_params import set_params
from optimize import optimize
from get_strategies import get_strategies
from generate_buy_signals import generate_buy_signals
from generate_sell_signals import generate_sell_signals
from technical_analysis import backtest
from indicators import calculate_rsi, calculate_sma

def main():
    # Cargar los conjuntos de datos
    datasets = {
        "5m": pd.read_csv("data/aapl_5m_train.csv"),
        "1m": pd.read_csv("data/aapl_1m_train.csv"),
        "1d": pd.read_csv("data/aapl_1d_train.csv"),
        "1h": pd.read_csv("data/aapl_1h_train.csv"),
    }

    # Resultados globales
    global_results = {}

    # Iterar sobre cada conjunto de datos
    for timeframe, data in datasets.items():
        print(f"Procesando datos de {timeframe}...")

        # Aplicar los indicadores técnicos necesarios
        data['RSI'] = calculate_rsi(data['close'], window=14)
        data['SMA'] = calculate_sma(data['close'], window=50)

        # Generar estrategias base
        strategies = get_strategies()

        # Generar señales de compra y venta
        data = generate_buy_signals(data, strategies)
        data = generate_sell_signals(data, strategies)

        # Optimizar estrategias
        study = optimize(data)

        # Realizar backtesting con la estrategia óptima
        results = backtest2(data, study.best_params)

        # Guardar los resultados para cada timeframe
        global_results[timeframe] = results

    # Analizar y presentar resultados globales


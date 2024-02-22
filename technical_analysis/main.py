import pandas as pd
from set_params import set_params
from optimize import optimize_strategy
from get_strategies import get_strategies
from generate_buy_signals import generate_buy_signals
from generate_sell_signals import generate_sell_signals
from backtest import backtest_strategy
from indicators import calculate_rsi, calculate_sma

# Cargar los conjuntos de datos
datasets = {
    "5m": pd.read_csv("data/aapl_5m_train.csv"),
    "1m": pd.read_csv("data/aapl_1m_train.csv"),
    "1d": pd.read_csv("data/aapl_1d_train.csv"),
    "1h": pd.read_csv("data/aapl_1h_train.csv"),
}

# Iterar sobre cada conjunto de datos
for timeframe, data in datasets.items():
    print(f"Procesando datos de {timeframe}...")

    # Aplicar los indicadores técnicos necesarios
    # Ejemplo:
    data['RSI'] = calculate_rsi(data['close'], period=14)
    data['SMA'] = calculate_sma(data['close'], window=50)

    # Generar estrategias base
    strategies = get_strategies()

    # Generar señales de compra y venta
    data = generate_buy_signals(data, strategies)
    data = generate_sell_signals(data, strategies)

    # Optimizar estrategias
    study = optimize_strategy(data, num_trials=100)

    # Realizar backtesting con la estrategia óptima
    results = backtest_strategy(data, study.best_params)

    # Analizar los resultados
    

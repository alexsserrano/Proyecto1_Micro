# main.py
import pandas as pd
from optimize import optimize
from get_strategies import get_strategies
from generate_buy_signals import generate_buy_signals
from generate_sell_signals import generate_sell_signals
from technical_analysis.backtest import backtest
from indicators import calculate_rsi, calculate_sma, calculate_bollinger, calculate_volume_oscillator
from set_params import set_params

# Cargar los conjuntos de datos
datasets = {
    "5m": pd.read_csv("data/aapl_5m_train.csv"),
    "1m": pd.read_csv("data/aapl_1m_train.csv"),
    "1d": pd.read_csv("data/aapl_1d_train.csv"),
    "1h": pd.read_csv("data/aapl_1h_train.csv"),
}

# Definir los resultados finales
final_results = []

# Iterar sobre cada conjunto de datos
for timeframe, data in datasets.items():
    print(f"Procesando datos de {timeframe}...")

    # Aplicar los indicadores técnicos necesarios
    data['RSI'] = calculate_rsi(data, window=14)
    data['SMA_short'], data['SMA_long'] = calculate_sma(data['close'], 5), calculate_sma(data['close'], 20)
    data['BB_mavg'], data['BB_hband'], data['BB_lband'] = calculate_bollinger(data, 20, 2)
    data['Volume_Osc'] = calculate_volume_oscillator(data, 5, 20)

    # Generar señales de compra y venta usando la estrategia óptima
    buy_signals = generate_buy_signals(data, optimal_strategy)
    sell_signals = generate_sell_signals(data, optimal_strategy)

    # Realizar backtesting con la estrategia óptima
    results = backtest(data, buy_signals, sell_signals, 10000, 0.001, 10, 0.01, 0.01)

    # Guardar los resultados
    final_results.append({"timeframe": timeframe, "results": results})

# Analizar y comparar los resultados
# Nota: Este paso puede implicar visualizar los resultados, comparar rendimientos entre diferentes timeframes,
# y potencialmente comparar contra una estrategia pasiva.
# El análisis detallado y las visualizaciones pueden ser realizados en un Jupyter Notebook como 'report.ipynb'.

# Ejemplo de cómo podrías imprimir un resumen de los resultados:
for result in final_results:
    print(f"Timeframe: {result['timeframe']}, Total Return: {result['results']['total_return']}")

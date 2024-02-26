import pandas as pd
from indicators import calculate_rsi, calculate_sma, calculate_bollinger,calculate_volume_oscillator
from generate_buy_signals import generate_buy_signals
from generate_sell_signals import generate_sell_signals
from backtest import backtest
from optimize import optimize


# Función principal para ejecutar la estrategia de trading
def run_trading_strategy(dataset_path):
    # Cargar el dataset
    data = pd.read_csv(dataset_path)

    # Calcular indicadores técnicos
    data = calculate_indicators(data)

    # Generar señales de compra/venta
    data = generate_signals(data)

    # Realizar backtesting de la estrategia
    results = backtest_strategy(data)

    # (Opcional) Optimizar parámetros de la estrategia
    optimized_results = optimize_parameters(data)

    return results, optimized_results


def calculate_indicators(data):
    # Aquí podrías llamar a las funciones de cálculo de indicadores específicos que ya has definido
    rsi = calculate_rsi(data)
    sma = calculate_sma(data['Close'], window=14)
    bollinger_bands = calculate_bollinger(data)
    volume_oscillator = calculate_volume_oscillator(data, short_window=10, long_window=20)

    # Luego puedes agregar estos indicadores al DataFrame 'data' o manejarlos como prefieras
    return data


if __name__ == "__main__":
    # Rutas a los datasets de prueba
    datasets = {
        "1d": "data/aapl_1d_test.csv",
        "1h": "data/aapl_1h_test.csv",
        "5m": "data/aapl_5m_test.csv",
        "1m": "data/aapl_1m_test.csv",
    }

    for timeframe, dataset_path in datasets.items():
        print(f"Running strategy for {timeframe} dataset")
        results, optimized_results = run_trading_strategy(dataset_path)
        print(f"Results for {timeframe}: {results}")
        # Aquí puedes guardar los resultados para su posterior análisis en report.ipynb

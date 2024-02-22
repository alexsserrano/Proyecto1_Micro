import pandas as pd


def backtest(data: pd.DataFrame, buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, initial_cash: float = 10000,
             commission_per_trade: float = 0.001):
    """
    Realiza el backtesting de estrategias de trading basadas en señales de compra y venta,
    calculando el rendimiento de la inversión sobre un conjunto de datos históricos.

    Parameters:
    - data (pd.DataFrame): DataFrame que contiene los datos de precios con una columna 'Close'.
    - buy_signals (pd.DataFrame): DataFrame con señales de compra para cada estrategia (1 para comprar, 0 en caso contrario).
    - sell_signals (pd.DataFrame): DataFrame con señales de venta para cada estrategia (1 para vender, 0 en caso contrario).
    - initial_cash (float): Capital inicial para el backtesting.
    - commission_per_trade (float): Comisión por operación como una fracción del volumen de la operación.

    Returns:
    - dict: Un diccionario con los resultados del backtesting, incluyendo el valor final de la cartera, el retorno total y la serie de tiempo del valor de la cartera.
    """
    cash = initial_cash
    shares_held = {col: 0 for col in buy_signals.columns}  # Diccionario para rastrear acciones compradas por estrategia
    portfolio_value = []

    for i in range(len(data)):
        for strategy in buy_signals.columns:
            # Comprar acciones basadas en la señal de compra y si hay efectivo disponible
            if buy_signals[strategy].iloc[i] == 1 and cash > data['Close'].iloc[i]:
                shares_to_buy = int(cash / data['Close'].iloc[i] / (1 + commission_per_trade))
                shares_held[strategy] += shares_to_buy
                cash -= shares_to_buy * data['Close'].iloc[i] * (1 + commission_per_trade)

            # Vender acciones basadas en la señal de venta
            if sell_signals[strategy].iloc[i] == 1 and shares_held[strategy] > 0:
                cash += shares_held[strategy] * data['Close'].iloc[i] * (1 - commission_per_trade)
                shares_held[strategy] = 0

        # Calcular el valor total de la cartera (efectivo + valor de las acciones)
        total_shares_value = sum(shares_held[strategy] * data['Close'].iloc[i] for strategy in shares_held)
        portfolio_value.append(cash + total_shares_value)

    final_portfolio_value = portfolio_value[-1]
    total_return = (final_portfolio_value - initial_cash) / initial_cash

    return {
        'initial_cash': initial_cash,
        'final_portfolio_value': final_portfolio_value,
        'total_return': total_return,
        'portfolio_value_over_time': portfolio_value
    }

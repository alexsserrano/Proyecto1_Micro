import pandas as pd
import matplotlib.pyplot as plt
from technical_analysis.indicators import calculate_rsi, calculate_sma
from utils.utils import Operation, backtest_strategy

def main():
    data = pd.read_csv("aapl_5m_train.csv")

    rsi_data = calculate_rsi(data, window=14)
    data["RSI"] = rsi_data

    short_ma = calculate_sma(data.Close, window=5)
    long_ma = calculate_sma(data.Close, window=21)

    data["SHORT_SMA"] = short_ma
    data["LONG_SMA"] = long_ma

    data = data.dropna()

    # Define initial variables
    cash = 1_000_000
    com = 0.00125
    n_shares = 40

    # Initialize buy/sell signals
    data["SMA_Sell_Signal"] = data.LONG_SMA > data.SHORT_SMA
    data["SMA_Buy_Signal"] = data.LONG_SMA < data.SHORT_SMA

    # Define the strategy function
    def strategy(row, active_operations):
        temp_operations = []

        for op in active_operations:
            if op.stop_loss > row.Close:
                cash += row.Close * op.n_shares * (1 - com)
            elif op.take_profit < row.Close:
                cash += row.Close * op.n_shares * (1 - com)
            else:
                temp_operations.append(op)

        active_operations = temp_operations

        if cash > row.Close * n_shares * (1 + com):
            if row.LONG_SMA < row.SHORT_SMA and not row.SMA_Buy_Signal:
                # Buy signal
                active_operations.append(Operation("long", row.Close, row.Timestamp, n_shares,
                                                    stop_loss=row.Close * 0.95, take_profit=row.Close * 1.05))
                cash -= row.Close * n_shares * (1 + com)
            elif row.LONG_SMA > row.SHORT_SMA:
                row.SMA_Buy_Signal = False

        return cash, active_operations

    # Perform backtesting
    strategy_value = backtest_strategy(data, strategy, cash, n_shares)

    # Plot results
    plt.figure(figsize=(12, 4))
    plt.plot(strategy_value)
    plt.title("First Trading Strategy")
    plt.show()

if __name__ == "__main__":
    main()

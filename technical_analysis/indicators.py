import ta

def calculate_rsi(data, window=14):
    rsi_data = ta.momentum.RSIIndicator(close=data.Close, window=window)
    return rsi_data.rsi()

def calculate_sma(close, window):
    return ta.trend.SMAIndicator(close=close, window=window).sma_indicator()

def calculate_bollinger(data, window, window_dev):
    bb_indicator = ta.volatility.BollingerBands(close=data.Close, window=window, window_dev=window_dev)
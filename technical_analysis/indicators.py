import ta

def calculate_rsi(data, window=14):
    rsi_data = ta.momentum.RSIIndicator(close=data.Close, window=window)
    return rsi_data.rsi()

def calculate_sma(close, window):
    """
    Calcula la Media Móvil Simple (SMA) para los datos proporcionados.

    Parameters:
    - close (pd.Series): Serie que contiene los precios de cierre.
    - window (int): El tamaño de la ventana para el cálculo de la SMA.

    Returns:
    - pd.Series: La SMA calculada.
    """
    return ta.trend.SMAIndicator(close=close, window=window).sma_indicator()


# def calculate_bollinger(data, window, window_dev):
#    bb_indicator = ta.volatility.BollingerBands(close=data.Close, window=window, window_dev=window_dev)

def calculate_bollinger(data, window=20, window_dev=2):
    """
    Calcula las Bandas de Bollinger para los datos proporcionados.

    Parameters:
    - data (pd.DataFrame): DataFrame que contiene los datos, debe incluir una columna 'Close'.
    - window (int): El tamaño de la ventana para el cálculo de las medias móviles.
    - window_dev (int): El número de desviaciones estándar para calcular la banda superior e inferior.

    Returns:
    - Tuple[pd.Series, pd.Series, pd.Series]: Un trío de series que contienen la banda media, superior e inferior, respectivamente.
    """
    bb_indicator = ta.volatility.BollingerBands(close=data.Close, window=window, window_dev=window_dev)
    return bb_indicator.bollinger_mavg(), bb_indicator.bollinger_hband(), bb_indicator.bollinger_lband()


def calculate_volume_oscillator(data, short_window, long_window):
    """
    Calcula el Oscilador de Volumen a partir de los datos proporcionados.

    Parameters:
    - data (pd.DataFrame): DataFrame que contiene los datos, debe incluir una columna 'Volume'.
    - short_window (int): El tamaño de la ventana para la media móvil de corto plazo del volumen.
    - long_window (int): El tamaño de la ventana para la media móvil de largo plazo del volumen.

    Returns:
    - pd.Series: El Oscilador de Volumen calculado como la diferencia entre la media móvil de corto plazo y la de largo plazo del volumen.
    """
    # Calcula la media móvil de corto plazo del volumen
    short_vol_ma = ta.trend.sma_indicator(close=data.Volume, window=short_window)

    # Calcula la media móvil de largo plazo del volumen
    long_vol_ma = ta.trend.sma_indicator(close=data.Volume, window=long_window)

    # Calcula el Oscilador de Volumen como la diferencia entre las dos medias móviles
    volume_oscillator = short_vol_ma - long_vol_ma

    return volume_oscillator

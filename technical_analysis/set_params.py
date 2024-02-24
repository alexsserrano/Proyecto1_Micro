def set_params(strategy: dict, **kwargs) -> dict:
    """
    Establece o ajusta los parámetros para los indicadores de una estrategia de trading.

    Parameters:
    - strategy (dict): Estrategia de trading a modificar. Debe contener un campo 'params' para cada indicador.
    - **kwargs: Parámetros específicos de los indicadores a ajustar, donde cada clave corresponde a un indicador
      y cada valor es un diccionario de los parámetros a ajustar para ese indicador.

    Returns:
    - dict: Estrategia de trading con los parámetros actualizados.
    """
    # Asegúrate de que la estrategia tiene un campo para parámetros; si no, inicialízalo
    if 'params' not in strategy:
        strategy['params'] = {}

    for indicator, params in kwargs.items():
        if indicator in strategy['indicators']:
            # Actualiza o agrega los parámetros específicos para el indicador
            strategy['params'][indicator] = params

    return strategy

# Ejemplo de uso con la estrategia que incluye múltiples indicadores
strategy_example = {
    'id': 1,
    'indicators': ['SMA', 'RSI'],
    'params': {}
}

# Ajustamos los parámetros de la estrategia
strategy_example = set_params(
    strategy_example,
    SMA={'short_window': 5, 'long_window': 20},
    RSI={'rsi_period': 14}
)

print(strategy_example)

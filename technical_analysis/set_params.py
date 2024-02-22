def set_params(strategy: dict, **kwargs) -> dict:
    """
    Establece o ajusta los parámetros para los indicadores de una estrategia de trading.

    Parameters:
    strategy (dict): Estrategia de trading a modificar.
    **kwargs: Parámetros específicos de los indicadores a ajustar.

    Returns:
    dict: Estrategia de trading con los parámetros actualizados.
    """
    # Asegúrate de que la estrategia tiene un campo para parámetros; si no, inicialízalo
    if 'params' not in strategy:
        strategy['params'] = {}

    for key, value in kwargs.items():
        # Actualiza o agrega el parámetro especificado
        strategy['params'][key] = value

    return strategy


# Ejemplo de estrategia
strategy_example = {'id': 1, 'indicators': ['SMA']}

# Ajustamos los parámetros de la estrategia, por ejemplo, el período de SMA
strategy_example = set_params(strategy_example, period=20, threshold=0.02)

print(strategy_example)

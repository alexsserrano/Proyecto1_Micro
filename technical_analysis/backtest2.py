import pandas as pd


class Operation:
    def _init_(self, operation_type, bought_at, shares, stop_loss=None, take_profit=None):
        self.operation_type = operation_type  # "long" o "short"
        self.bought_at = bought_at
        self.shares = shares
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.closed = False

def backtest(data: pd.DataFrame, buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, initial_cash: float = 10000,
             commission_per_trade: float = 0.001, shares_to_operate: int = 10, stop_loss: float = 0.01,
             take_profit: float = 0.01):
    cash = initial_cash
    active_operations = []
    portfolio_value = []

    for i in range(len(data)):
        current_price = data['Close'].iloc[i]

        # Cerrar operaciones basadas en stop_loss, take_profit o señal de venta
        for op in active_operations:
            if not op.closed:
                if op.operation_type == "long":
                    if (current_price <= op.bought_at * (1 - stop_loss)) or (current_price >= op.bought_at * (1 + take_profit)) or (sell_signals.iloc[i]):
                        cash += current_price * op.shares * (1 - commission_per_trade)
                        op.closed = True
                elif op.operation_type == "short":
                    if (current_price >= op.bought_at * (1 + stop_loss)) or (current_price <= op.bought_at * (1 - take_profit)) or (buy_signals.iloc[i]):
                        cash += (op.bought_at * 2 - current_price) * op.shares * (1 - commission_per_trade)  # Simplificación del cálculo para una operación corta
                        op.closed = True

        # Eliminar operaciones cerradas de la lista activa
        active_operations = [op for op in active_operations if not op.closed]

        # Abrir nuevas operaciones basadas en señales de compra
        if buy_signals.iloc[i] and cash >= current_price * shares_to_operate * (1 + commission_per_trade):
            cash -= current_price * shares_to_operate * (1 + commission_per_trade)
            new_op = Operation("long", current_price, shares_to_operate, stop_loss, take_profit)
            active_operations.append(new_op)

        # (Opcional) Manejar operaciones cortas aquí, si las señales correspondientes están definidas

        # Calcular el valor total de la cartera (efectivo + valor de las acciones activas)
        total_shares_value = sum(op.shares * current_price for op in active_operations if not op.closed)
        portfolio_value.append(cash + total_shares_value)

    final_portfolio_value = portfolio_value[-1]
    total_return = (final_portfolio_value - initial_cash) / initial_cash

    return {
        'initial_cash': initial_cash,
        'final_portfolio_value': final_portfolio_value,
        'total_return': total_return,
        'portfolio_value_over_time': portfolio_value
    }

class Operation:
    def __init__(self, operation_type, bought_at, timestamp,
                 n_shares, stop_loss, take_profit):
        self.operation_type = operation_type
        self.bought_at = bought_at
        self.timestamp = timestamp
        self.n_shares = n_shares
        self.sold_at = None
        self.stop_loss = stop_loss
        self.take_profit = take_profit

def backtest_strategy(data, strategy_func, initial_cash, n_shares):
    cash = initial_cash
    active_operations = []
    com = 0.00125
    strategy_value = [initial_cash]

    for i, row in data.iterrows():
        cash, active_operations = strategy_func(row, active_operations)

        total_value = len(active_operations) * row.Close * n_shares
        strategy_value.append(cash + total_value)

    return strategy_value

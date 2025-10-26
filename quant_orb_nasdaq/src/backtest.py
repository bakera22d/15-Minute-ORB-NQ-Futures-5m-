import pandas as pd
import numpy as np

def backtest_orb(data: pd.DataFrame, signals: pd.DataFrame, stop_loss: float = 0.003, take_profit: float = 0.006):
    """
    Backtest ORB signals using fixed stop-loss and take-profit percentages.
    """
    df = data.copy()
    trades = []

    for _, sig in signals.iterrows():
        entry_time = sig["Datetime"]
        side = sig["Signal"]

        # Ensure scalar entry price
        if entry_time not in df.index:
            continue
        entry_val = df.loc[entry_time, "Close"]
        entry_price = float(entry_val.iloc[0]) if isinstance(entry_val, pd.Series) else float(entry_val)

        # Slice from entry onward
        subsequent = df.loc[entry_time:].copy()
        exit_price = entry_price

        for _, row in subsequent.iterrows():
            high = float(row["High"])
            low = float(row["Low"])

            # Directional move relative to entry
            move = (high - entry_price) / entry_price if side == 1 else (entry_price - low) / entry_price

            # Take-profit or stop-loss
            if move >= take_profit:
                exit_price = entry_price * (1 + take_profit * side)
                break
            elif move <= -stop_loss:
                exit_price = entry_price * (1 - stop_loss * side)
                break

        trade_return = (exit_price - entry_price) / entry_price * side
        trades.append(trade_return)

    results = pd.DataFrame({"Return": trades})

    if not results.empty:
        results["Cumulative"] = (1 + results["Return"]).cumprod()
        std = results["Return"].std()
        sharpe = (results["Return"].mean() / std) * np.sqrt(252) if std != 0 else None
        max_dd = (results["Cumulative"].cummax() - results["Cumulative"]).max()
    else:
        results["Cumulative"] = []
        sharpe = None
        max_dd = None

    return results, sharpe, max_dd


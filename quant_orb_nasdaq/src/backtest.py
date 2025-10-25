import pandas as pd

def backtest_orb(data: pd.DataFrame, signals: pd.DataFrame, stop_loss: float = 0.003, take_profit: float = 0.006):
    """
    Backtest ORB signals using fixed stop‑loss and take‑profit percentages.

    Parameters
    ----------
    data : pandas.DataFrame
        Intraday OHLC data with a datetime index.
    signals : pandas.DataFrame
        DataFrame returned by generate_orb_signals with at least 'Datetime' and 'Signal'.
    stop_loss : float
        Stop‑loss percentage (e.g., 0.003 = 0.3%).
    take_profit : float
        Take‑profit percentage (e.g., 0.006 = 0.6%).

    Returns
    -------
    results : pandas.DataFrame
        DataFrame with columns 'Return' and 'Cumulative' representing each trade's return and cumulative equity.
    sharpe : float or None
        Annualized Sharpe ratio (may be None if variance is zero or no trades).
    mdd : float or None
        Maximum drawdown (may be None if no trades).
    """
    df = data.copy()
    trades = []
    for _, sig in signals.iterrows():
        entry_time = sig["Datetime"]
        side = sig["Signal"]
        if entry_time not in df.index:
            continue
        entry_price = df.loc[entry_time, "Close"]
        subsequent = df.loc[entry_time:]
        exit_price = entry_price
        for _, row in subsequent.iterrows():
            move = (row["High"] - entry_price) / entry_price if side == 1 else (entry_price - row["Low"]) / entry_price
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
        sharpe = (results["Return"].mean() / std) * (252 ** 0.5) if std != 0 else None
        max_dd = (results["Cumulative"].cummax() - results["Cumulative"]).max()
    else:
        results["Cumulative"] = []
        sharpe = None
        max_dd = None
    return results, sharpe, max_dd

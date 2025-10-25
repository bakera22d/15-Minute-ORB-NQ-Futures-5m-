import pandas as pd

def generate_orb_signals(data: pd.DataFrame, open_time: str = "09:30", close_time: str = "16:00") -> pd.DataFrame:
    """
    Generate trading signals for a 15-minute Opening Range Breakout (ORB) strategy.

    A breakout is defined as the first instance when price trades above or below the
    highest or lowest price of the 9:30–9:45 session.

    Parameters
    ----------
    data : pandas.DataFrame
        Intraday OHLC data with a datetime index.
    open_time : str
        Start of the regular session (default "09:30").
    close_time : str
        End of the session (default "16:00").

    Returns
    -------
    pandas.DataFrame
        DataFrame containing one row per breakout event with columns:
        'Datetime', 'Signal' (1 for long, -1 for short), 'ORB_High', and 'ORB_Low'.
    """
    df = data.copy()
    df["Date"] = df.index.date
    signals = []
    for date, day_data in df.groupby("Date"):
        session_data = day_data.between_time(open_time, close_time)
        if session_data.empty:
            continue
        orb_range = session_data.between_time("09:30", "09:45")
        if orb_range.empty:
            continue
        high = orb_range["High"].max()
        low = orb_range["Low"].min()
        post_orb = session_data.between_time("09:45", close_time)
        if post_orb.empty:
            continue
        breakout_time = None
        side = 0
        for ts, row in post_orb.iterrows():
            if row["High"] > high:
                breakout_time = ts
                side = 1
                break
            elif row["Low"] < low:
                breakout_time = ts
                side = -1
                break
        if breakout_time:
            signals.append({
                "Datetime": breakout_time,
                "Signal": side,
                "ORB_High": high,
                "ORB_Low": low
            })
    return pd.DataFrame(signals)

import pandas as pd

def generate_orb_signals(data, open_time="09:30", close_time="16:00"):
    """Generate Opening Range Breakout (ORB) buy/sell signals for each session."""
    df = data.copy()
    df["Date"] = df.index.date
    signals = []

    for date, day_data in df.groupby("Date"):
        # Ensure time index for slicing
        day_data = day_data.between_time(open_time, close_time)
        if day_data.empty:
            continue

        # 9:30–9:45 range
        orb_range = day_data.between_time("09:30", "09:45")
        if orb_range.empty:
            continue

        high = orb_range["High"].max()
        low = orb_range["Low"].min()

        # first breakout after 9:45
        post_orb = day_data.between_time("09:45", "16:00")
        if post_orb.empty:
            continue

        breakout_idx = None
        for i, row in post_orb.iterrows():
            if row["High"] > high:
                breakout_idx = i
                side = 1
                break
            elif row["Low"] < low:
                breakout_idx = i
                side = -1
                break

        if breakout_idx:
            signals.append({
                "Datetime": breakout_idx,
                "Signal": side,
                "ORB_High": high,
                "ORB_Low": low
            })

    return pd.DataFrame(signals)



import pandas as pd
def generate_orb_signals(data, open_time="09:30", close_time="16:00"):
    """Generate 15-minute Opening Range Breakout (ORB) buy/sell signals for each trading day."""
    df = data.copy()
    df["Date"] = df.index.date
    signals = []

    for date, day_data in df.groupby("Date"):
        day_data = day_data.between_time(open_time, close_time)
        if day_data.empty:
            continue

        # 9:30–9:45 range
        orb_range = day_data.between_time("09:30", "09:45")
        if orb_range.empty:
            continue

        high = float(orb_range["High"].max())
        low = float(orb_range["Low"].min())

        # Slice after 9:45
        post_orb = day_data.between_time("09:45", close_time)
        if post_orb.empty:
            continue

        breakout_idx = None
        side = 0
        for i in range(len(post_orb)):
            # Explicit scalar extraction using .iloc[]
            bar_high = float(post_orb["High"].iloc[i])
            bar_low = float(post_orb["Low"].iloc[i])

            if bar_high > high:
                breakout_idx = post_orb.index[i]
                side = 1
                break
            elif bar_low < low:
                breakout_idx = post_orb.index[i]
                side = -1
                break

        if breakout_idx is not None:
            signals.append({
                "Datetime": breakout_idx,
                "Signal": side,
                "ORB_High": high,
                "ORB_Low": low
            })

    return pd.DataFrame(signals)

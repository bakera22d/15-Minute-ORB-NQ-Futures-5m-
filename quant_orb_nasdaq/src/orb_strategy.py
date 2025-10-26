import pandas as pd

def generate_orb_signals(data, open_time="09:30", close_time="16:00"):
    """Generate 15-minute Opening Range Breakout (ORB) buy/sell signals for each trading day,
    with time zone localization and weekend/incomplete-session filtering."""

    df = data.copy()

    # --- Remove weekends ---
    df = df[df.index.dayofweek < 5]  # 0=Monday, 6=Sunday

    # --- Add Date column for grouping ---
    df["Date"] = df.index.date
    signals = []

    # --- Process each trading day separately ---
    for date, day_data in df.groupby("Date"):
        # Only consider regular market hours
        day_data = day_data.between_time(open_time, close_time)
        if day_data.empty or len(day_data) < 30:
            continue  # skip incomplete or holiday sessions

        # 9:30–9:45 opening range
        orb_range = day_data.between_time("09:30", "09:45")
        if orb_range.empty:
            continue

        high = float(orb_range["High"].max())
        low = float(orb_range["Low"].min())

        # Slice after 9:45 to find breakout
        post_orb = day_data.between_time("09:45", close_time)
        if post_orb.empty:
            continue

        breakout_idx = None
        side = 0

        # Find first breakout candle
        for i in range(len(post_orb)):
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

        # Store signal
        if breakout_idx is not None:
            signals.append({
                "Datetime": breakout_idx,
                "Signal": side,
                "ORB_High": high,
                "ORB_Low": low
            })

    return pd.DataFrame(signals) into this

import yfinance as yf
import pandas as pd

def load_nq_data(start: str | None = None, end: str | None = None, interval: str = "5m", period: str | None = None) -> pd.DataFrame:
    """
    Load NASDAQ futures (NQ=F) intraday data from Yahoo Finance.

    Parameters
    ----------
    start : str or None
        The start date in 'YYYY-MM-DD' format. Ignored if period is provided.
    end : str or None
        The end date in 'YYYY-MM-DD' format. Ignored if period is provided.
    interval : str
        Bar interval. Default is '5m'.
    period : str or None
        Data range, e.g., '45d'. When provided, Yahoo's period parameter is used
        and start/end are ignored.

    Returns
    -------
    pandas.DataFrame
        DataFrame with datetime index and columns ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
    """
    if period:
        data = yf.download("NQ=F", period=period, interval=interval)
    else:
        data = yf.download("NQ=F", start=start, end=end, interval=interval)
    data = data.dropna()
    # Remove timezone from index for consistency
    if getattr(data.index, 'tz', None):
        data.index = data.index.tz_localize(None)
    return data

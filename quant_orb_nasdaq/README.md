# NASDAQ 15-Minute Opening Range Breakout (ORB) Strategy

This repository contains a Python implementation of a **15‑minute Opening Range Breakout (ORB)** trading strategy for NASDAQ futures (symbol `NQ=F`).  The strategy defines the opening range as the highest and lowest prices observed during the first 15 minutes of the regular U.S. trading session (9:30–9:45 America/New_York time).  When price breaks above this range, a long trade is entered; if price breaks below, a short trade is entered.  Each trade uses a configurable stop‑loss and take‑profit level.  The project includes:

* A **data loader** using `yfinance` to download intraday data (5‑minute bars).
* A **signal generator** to detect the first breakout of the opening range.
* A **simple backtest engine** applying stop‑loss and take‑profit rules.
* A **Streamlit dashboard** to run the strategy and visualize performance interactively.

> **Note on data range:** Yahoo Finance restricts intraday data (like 5‑minute bars) to roughly the past 60 days.  Use the `period="45d"` option in the dashboard or loader to ensure data is available.  For longer histories or other instruments, consider connecting to a premium data provider.

## Getting Started

### Installation

Create a virtual environment (optional but recommended) and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Strategy Locally

You can run the backtest directly from Python or via the Streamlit dashboard:

```bash
streamlit run app.py
```

1. Launching the app opens a browser window.
2. Select **Recent 45 days** or define custom start/end dates.
3. Click **Run Backtest** to generate signals, compute performance metrics (Sharpe ratio and maximum drawdown), and display the cumulative equity curve.

### Project Structure

```
quant_orb_nasdaq/
├── app.py                 # Streamlit dashboard
├── requirements.txt       # Library dependencies
├── README.md              # Project overview and instructions
└── src/
    ├── data_loader.py     # Data fetching utilities
    ├── orb_strategy.py    # 15‑min ORB signal generation
    ├── backtest.py        # Backtesting logic and metrics
    └── visualize.py       # Plotly chart helper
```

### Customization

* **Stop‑loss / take‑profit:** adjust the `stop_loss` and `take_profit` parameters in `backtest.py`.
* **Time range:** modify `open_time` and `close_time` in `orb_strategy.py` for other markets or sessions.
* **Data source:** switch to a different API (e.g. Polygon.io, Alpaca) in `src/data_loader.py` if you need a longer intraday history.

### Deployment to Streamlit Community Cloud

1. Push this repository to a public GitHub repo.
2. Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Create a new app, connect your GitHub repo, and select `app.py` as the entry point.
4. Streamlit Cloud will install the dependencies and host your app for free, giving you a shareable URL.

## License

This project is provided for educational purposes and is not financial advice.  Use at your own risk.

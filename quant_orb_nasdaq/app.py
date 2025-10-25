import streamlit as st
import pandas as pd

from src.data_loader import load_nq_data
from src.orb_strategy import generate_orb_signals
from src.backtest import backtest_orb
from src.visualize import plot_equity_curve

# ----------------------------------------------------------
# Streamlit configuration
# ----------------------------------------------------------
st.set_page_config(
    page_title="NASDAQ 15-Min ORB Strategy",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("NASDAQ Futures 15-Minute Opening Range Breakout (ORB) Strategy")

st.markdown(
    """
    This app implements a 15-minute Opening Range Breakout strategy on NASDAQ futures (symbol `NQ=F`).

    Select a time range below, then click **Run Backtest** to generate signals, compute the strategy's
    performance, and visualize the cumulative equity curve.
    """
)

# ----------------------------------------------------------
# Sidebar inputs
# ----------------------------------------------------------
with st.sidebar:
    st.header("Data Parameters")
    mode = st.selectbox("Data Mode", ["Recent 45 days", "Custom dates"])
    if mode == "Custom dates":
        start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
        end_date = st.date_input("End date", pd.to_datetime("2024-02-01"))
        if start_date >= end_date:
            st.error("Start date must be before end date.")
    else:
        start_date = None
        end_date = None

    st.header("Trade Parameters")
    stop_loss_pct = st.number_input("Stop-loss (%)", min_value=0.1, max_value=5.0, value=0.3, step=0.1)
    take_profit_pct = st.number_input("Take-profit (%)", min_value=0.1, max_value=5.0, value=0.6, step=0.1)

# ----------------------------------------------------------
# Run backtest
# ----------------------------------------------------------
if st.button("Run Backtest"):
    with st.spinner("Loading data..."):
        if mode == "Custom dates":
            df = load_nq_data(start=str(start_date), end=str(end_date), interval="5m")
        else:
            df = load_nq_data(period="45d", interval="5m")

    if df is None or df.empty:
        st.error("No data available for the selected range.")
    else:
        st.success(f"Loaded {len(df)} bars of data.")

        with st.spinner("Generating signals..."):
            signals = generate_orb_signals(df)

        if signals.empty:
            st.warning("No breakout signals were generated for the selected range.")
        else:
            st.success(f"Generated {len(signals)} signals.")

            with st.spinner("Running backtest..."):
                results, sharpe, max_dd = backtest_orb(
                    df,
                    signals,
                    stop_loss=stop_loss_pct / 100,
                    take_profit=take_profit_pct / 100
                )

                # ----------------------------------------------------------
                # Calculate extra metrics
                # ----------------------------------------------------------
                total_return = results["Cumulative"].iloc[-1] - 1 if not results.empty else 0
                win_rate = (results["Return"] > 0).mean() if not results.empty else 0
                avg_trade = results["Return"].mean() if not results.empty else 0

                # ----------------------------------------------------------
                # KPI display
                # ----------------------------------------------------------
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric("Total Trades", f"{len(results)}")
                col2.metric("Total Return", f"{total_return:.2%}")
                col3.metric("Win Rate", f"{win_rate:.2%}")
                col4.metric("Avg Trade Return", f"{avg_trade:.2%}")
                col5.metric("Sharpe Ratio", f"{sharpe:.2f}" if sharpe is not None else "N/A")
                col6.metric("Max Drawdown", f"{max_dd:.2%}" if max_dd is not None else "N/A")

                # ----------------------------------------------------------
                # Equity curve chart
                # ----------------------------------------------------------
                st.subheader("ORB Strategy Cumulative Performance")
                fig = plot_equity_curve(results)
                st.plotly_chart(fig, use_container_width=True)

                # ----------------------------------------------------------
                # Data outputs
                # ----------------------------------------------------------
                with st.expander("Show trade returns"):
                    st.dataframe(results)
                with st.expander("Show signals"):
                    st.dataframe(signals)

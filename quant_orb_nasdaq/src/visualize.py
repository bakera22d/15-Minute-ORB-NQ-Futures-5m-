import plotly.graph_objects as go

def plot_equity_curve(results):
    """
    Create a Plotly figure showing the cumulative equity curve.

    Parameters
    ----------
    results : pandas.DataFrame
        DataFrame containing 'Cumulative' column as returned by backtest_orb.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure with the equity curve.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=results["Cumulative"],
        mode="lines",
        name="Equity Curve"
    ))
    fig.update_layout(
        title="ORB Strategy Cumulative Performance",
        xaxis_title="Trade #",
        yaxis_title="Cumulative Return",
        template="plotly_dark"
    )
    return fig

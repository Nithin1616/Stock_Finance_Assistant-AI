import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def create_price_chart(hist_df: pd.DataFrame, ticker: str, company_name: str) -> go.Figure:
    """Create an interactive candlestick + line chart."""
    if hist_df.empty:
        return None

    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=hist_df.index,
        open=hist_df["Open"],
        high=hist_df["High"],
        low=hist_df["Low"],
        close=hist_df["Close"],
        name="Price",
        increasing_line_color="#00C896",
        decreasing_line_color="#FF4B6E",
    ))

    # Volume bar chart (secondary y-axis)
    fig.add_trace(go.Bar(
        x=hist_df.index,
        y=hist_df["Volume"],
        name="Volume",
        yaxis="y2",
        opacity=0.3,
        marker_color="#4A90D9",
    ))

    fig.update_layout(
        title=f"{company_name} ({ticker}) - Price History",
        title_font_size=16,
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#0D1117",
        font=dict(color="#E6EDF3"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis_rangeslider_visible=False,
        height=450,
    )

    return fig


def create_moving_average_chart(hist_df: pd.DataFrame, ticker: str) -> go.Figure:
    """Create a line chart with moving averages."""
    if hist_df.empty:
        return None

    # Calculate moving averages
    hist_df = hist_df.copy()
    hist_df["MA20"] = hist_df["Close"].rolling(window=20).mean()
    hist_df["MA50"] = hist_df["Close"].rolling(window=50).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist_df.index,
        y=hist_df["Close"],
        name="Close Price",
        line=dict(color="#4A90D9", width=2),
    ))

    fig.add_trace(go.Scatter(
        x=hist_df.index,
        y=hist_df["MA20"],
        name="20-Day MA",
        line=dict(color="#F5A623", width=1.5, dash="dash"),
    ))

    fig.add_trace(go.Scatter(
        x=hist_df.index,
        y=hist_df["MA50"],
        name="50-Day MA",
        line=dict(color="#FF4B6E", width=1.5, dash="dash"),
    ))

    fig.update_layout(
        title=f"{ticker} - Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#0D1117",
        font=dict(color="#E6EDF3"),
        height=350,
    )

    return fig


def create_metrics_gauge(current_price: float, week_low: float, week_high: float) -> go.Figure:
    """Create a gauge chart showing where current price sits in 52-week range."""
    try:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_price,
            title={"text": "52-Week Range Position", "font": {"color": "#E6EDF3"}},
            gauge={
                "axis": {"range": [week_low, week_high], "tickcolor": "#E6EDF3"},
                "bar": {"color": "#4A90D9"},
                "bgcolor": "#1C2128",
                "bordercolor": "#30363D",
                "steps": [
                    {"range": [week_low, week_low + (week_high - week_low) * 0.33], "color": "#FF4B6E"},
                    {"range": [week_low + (week_high - week_low) * 0.33, week_low + (week_high - week_low) * 0.66], "color": "#F5A623"},
                    {"range": [week_low + (week_high - week_low) * 0.66, week_high], "color": "#00C896"},
                ],
            },
            number={"font": {"color": "#E6EDF3"}},
        ))

        fig.update_layout(
            paper_bgcolor="#0D1117",
            font=dict(color="#E6EDF3"),
            height=250,
            margin=dict(l=20, r=20, t=50, b=20),
        )

        return fig
    except:
        return None
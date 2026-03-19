import pandas as pd
import streamlit as st

try:
    import plotly.graph_objects as go  # type: ignore
except ModuleNotFoundError:
    go = None  # type: ignore


def plot_trend(df):
    chart_df = df.copy()
    chart_df["Time"] = pd.to_datetime(chart_df["Time"])
    chart_df["Score"] = chart_df["Score"].astype(str).str.lower()
    if chart_df.empty:
        st.info("No valid score data available.")
        return

    recent_date = chart_df["Time"].max()
    start_date = recent_date - pd.Timedelta(days=6)

    chart_df = chart_df[
        (chart_df["Time"] >= start_date) & (chart_df["Time"] <= recent_date)
    ].sort_values(by="Time")

    if chart_df.empty:
        st.info("No score records found in the last 7 days.")
        return

    color_map = {
        "poor": "red",
        "average": "orange",
        "normal": "gold",
        "good": "green",
    }
    chart_df["color"] = chart_df["Score"].map(color_map).fillna("gray")

    # Fall back if plotly isn't installed in the frontend container.
    if go is None:
        chart_df = chart_df.sort_values("Time")
        st.line_chart(chart_df.set_index("Time")["Score_num"], height=420)
        return

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_df["Time"],
            y=chart_df["Score_num"],
            mode="lines+markers",
            marker=dict(size=12, color=chart_df["color"]),
            text=chart_df["Score"],
            line=dict(width=2),
            hovertemplate=(
                "<b>Date</b>: %{x|%Y-%m-%d %H:%M}<br>"
                "<b>Score</b>: %{text}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="Mental Health Trend (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Score Level",
        xaxis=dict(tickformat="%Y-%m-%d"),
        yaxis=dict(
            tickvals=[1, 2, 3, 4],
            ticktext=["Poor", "Average", "Normal", "Good"],
            range=[0.8, 4.2],
        ),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        height=420,
    )
    st.plotly_chart(fig, width="stretch")

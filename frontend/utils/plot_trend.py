import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def plot_trend(df):
    df = df.copy()
    df["Time"] = pd.to_datetime(df["Time"])
    recent_date = df["Time"].max()
    start_date = recent_date - pd.Timedelta(days=6)
    df_filtered = df[(df["Time"] >= start_date) & (df["Time"] <= recent_date)]
    df_filtered = df_filtered.sort_values(by="Time")
    color_map = {
        "poor": "red",
        "average": "orange",
        "normal": "yellow",
        "good": "green",
    }
    # Map Score values to colors
    df_filtered["color"] = df_filtered["Score"].map(color_map)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_filtered["Time"],
            y=df_filtered["Score_num"],
            mode="lines+markers",
            marker=dict(size=12, color=df_filtered["color"]),
            text=df_filtered["Score"],
            line=dict(width=2),
        )
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Score",
        xaxis=dict(tickformat="%Y-%m-%d"),
        yaxis=dict(
            tickvals=[1, 2, 3, 4], ticktext=["poor", "average", "normal", "good"]
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

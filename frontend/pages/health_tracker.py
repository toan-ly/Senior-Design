from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from components.auth_guard import require_login
from components.sidebar import sidebar
from utils.api import get_scores
from utils.plot_trend import plot_trend

import pandas as pd


st.set_page_config(page_title="Health Tracker", page_icon="📈", layout="wide")
sidebar()
require_login()


SCORE_TO_NUM = {
    "poor": 1,
    "average": 2,
    "normal": 3,
    "good": 4,
}


def _parse_time(t: str) -> Optional[datetime]:
    if not t:
        return None
    try:
        return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


st.title("📈 Health Tracker")

username = st.session_state.get("username", "Guest")
access_token = st.session_state.get("access_token")

resp: Dict[str, Any] = get_scores(username=username, access_token=access_token)
items: List[Dict[str, Any]] = resp.get("items", []) if resp else []

if not items:
    st.info("No saved health assessments yet. Ask the assistant in Chat first.")
    st.stop()

# Sort by time ascending for trend chart.
items_sorted = sorted(
    items,
    key=lambda x: _parse_time(x.get("time", "")) or datetime.min,
)

latest = items_sorted[-1]
st.subheader("Latest Assessment")
st.markdown(
    f"**Time:** {latest.get('time', '')}\n\n"
    f"**Score:** {latest.get('score', '')}\n\n"
    f"**Total guess:** {latest.get('total_guess', '')}"
)

with st.expander("View details", expanded=False):
    st.write(latest.get("content", ""))

st.divider()
st.subheader("History")
table_rows = []
for x in items_sorted[::-1]:  # latest first
    table_rows.append(
        {
            "time": x.get("time", ""),
            "score": x.get("score", ""),
            "total_guess": x.get("total_guess", ""),
        }
    )
st.table(table_rows)

st.subheader("Trend")
# times = []
# numeric_scores = []
# for x in items_sorted:
#     t = _parse_time(x.get("time", ""))
#     if not t:
#         continue
#     times.append(t.isoformat(timespec="seconds"))
#     numeric_scores.append(SCORE_TO_NUM.get(str(x.get("score", "")).lower(), None))

# # Keep only valid points for chart.
# chart_times = []
# chart_scores = []
# for t, s in zip(times, numeric_scores):
#     if s is not None:
#         chart_times.append(t)
#         chart_scores.append(s)

# if chart_scores:
#     st.line_chart(chart_scores)
# else:
#     st.caption("No plottable numeric scores found (expected poor/average/normal/good).")

df = pd.DataFrame(items_sorted)
df = df.rename(columns={"time": "Time", "score": "Score"})
df["Score_num"] = df["Score"].astype(str).str.lower().map(SCORE_TO_NUM)
df = df.dropna(subset=["Time", "Score", "Score_num"])
if df.empty:
    st.caption("No plottable numeric scores found.")
else:
    plot_trend(df)

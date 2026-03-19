import calendar
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from components.auth_guard import require_login
from components.footer import footer
from components.sidebar import sidebar
from utils.api import get_journal_month, upsert_journal_entry


st.set_page_config(page_title="Journal", page_icon="📝", layout="wide")
sidebar()
require_login()

# ---- Mood style ----
MOOD_META = {
    "great": {"label": "Great", "icon": "😊", "color": "#00c853"},
    "good": {"label": "Good", "icon": "🙂", "color": "#8bc34a"},
    "okay": {"label": "Okay", "icon": "😐", "color": "#ffea00"},
    "bad": {"label": "Bad", "icon": "😕", "color": "#ffb300"},
    "mad": {"label": "Mad", "icon": "😠", "color": "#ff0000"},
    "sad": {"label": "Sad", "icon": "😢", "color": "#29b6f6"},
}

MOOD_ORDER = ["great", "good", "okay", "bad", "mad", "sad"]

st.markdown(
    """
    <style>
    .selected-mood-badge {
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
        margin-bottom: 4px;
        border: 2px solid #f5a3d7;
        background: #2a2a2a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---- Helpers ----
def _month_str(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def _date_str(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _parse_date(date_str: str) -> Optional[date]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# ---- Session state init ----
today = date.today()
st.session_state.setdefault("journal_month_base", today.replace(day=1))
st.session_state.setdefault("journal_selected_date", today)
st.session_state.setdefault("journal_show_reflection", False)
st.session_state.setdefault("journal_mood", "great")


# ---- Load entries for month ----
selected_date: date = st.session_state["journal_selected_date"]
month_base: date = st.session_state["journal_month_base"]
month = _month_str(month_base)

username = st.session_state.get("username", "Guest")
access_token = st.session_state.get("access_token")

month_resp: Dict[str, Any] = get_journal_month(
    username=username,
    month=month,
    access_token=access_token,
)
month_items: List[Dict[str, Any]] = month_resp.get("items", []) if month_resp else []
entries_by_date: Dict[str, Dict[str, Any]] = {
    x.get("date"): x for x in month_items if x.get("date")
}

# ---- Layout ----
col_left, col_right = st.columns([1.1, 1.5])

with col_left:
    st.markdown("### Daily Journal")
    st.caption(selected_date.strftime("%A, %B %d, %Y"))

    existing_entry = entries_by_date.get(_date_str(selected_date), {})

    # ---- Mood selector (3 columns) ----
    st.markdown("#### Mood")
    mood_selected = (
        existing_entry.get("mood") or st.session_state.get("journal_mood") or "great"
    )
    st.session_state["journal_mood"] = mood_selected

    for i in range(0, len(MOOD_ORDER), 3):
        cols = st.columns(3)
        row_keys = MOOD_ORDER[i : i + 3]

        for col, mood_key in zip(cols, row_keys):
            meta = MOOD_META[mood_key]
            with col:
                button_label = f"{meta['icon']} {meta['label']}"
                if st.button(
                    button_label,
                    key=f"mood_{mood_key}",
                    use_container_width=True,
                ):
                    st.session_state["journal_mood"] = mood_key
                    mood_selected = mood_key

    selected_meta = MOOD_META[st.session_state["journal_mood"]]
    st.markdown(
        f"""
        <div class="selected-mood-badge" style="color: {selected_meta["color"]};">
            Selected mood: {selected_meta["icon"]} {selected_meta["label"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Journal entry ----
    st.markdown("#### Journal Entry")
    journal_text_default = existing_entry.get("journal_text") or ""
    journal_text = st.text_area(
        "Write your thoughts...",
        value=journal_text_default,
        key=f"journal_text_{_date_str(selected_date)}",
        height=160,
        label_visibility="collapsed",
    )

    # ---- Reflection ----
    st.markdown("")
    if st.button("Add Reflection!", key="toggle_reflection"):
        st.session_state["journal_show_reflection"] = True

    if st.session_state.get("journal_show_reflection", False):
        reflection_default = existing_entry.get("reflection_text") or ""
        reflection_text = st.text_area(
            "Reflection (optional)",
            value=reflection_default,
            key=f"reflection_text_{_date_str(selected_date)}",
            height=90,
        )
    else:
        reflection_text = None

    # ---- Save ----
    if st.button("Save Entry", type="primary", key="save_entry"):
        upsert_journal_entry(
            username=username,
            date=_date_str(selected_date),
            mood=st.session_state["journal_mood"],
            journal_text=journal_text,
            reflection_text=reflection_text,
            access_token=access_token,
        )
        st.success("Journal entry saved.")
        st.rerun()

with col_right:
    st.markdown("###")
    st.subheader(month_base.strftime("%B %Y"))

    nav_prev, nav_next = st.columns(2)

    with nav_prev:
        if st.button("◀ Prev", key="month_prev"):
            y, m = month_base.year, month_base.month
            if m == 1:
                month_base = date(y - 1, 12, 1)
            else:
                month_base = date(y, m - 1, 1)
            st.session_state["journal_month_base"] = month_base
            selected_day = st.session_state["journal_selected_date"].day
            days_in_new_month = calendar.monthrange(month_base.year, month_base.month)[
                1
            ]
            st.session_state["journal_selected_date"] = date(
                month_base.year,
                month_base.month,
                min(selected_day, days_in_new_month),
            )
            st.rerun()

    with nav_next:
        if st.button("Next ▶", key="month_next"):
            y, m = month_base.year, month_base.month
            if m == 12:
                month_base = date(y + 1, 1, 1)
            else:
                month_base = date(y, m + 1, 1)
            st.session_state["journal_month_base"] = month_base
            selected_day = st.session_state["journal_selected_date"].day
            days_in_new_month = calendar.monthrange(month_base.year, month_base.month)[
                1
            ]
            st.session_state["journal_selected_date"] = date(
                month_base.year,
                month_base.month,
                min(selected_day, days_in_new_month),
            )
            st.rerun()

    days_in_month = calendar.monthrange(month_base.year, month_base.month)[1]
    start_weekday = calendar.monthrange(month_base.year, month_base.month)[0]

    st.markdown("####")
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)
    for idx, wd in enumerate(weekdays):
        header_cols[idx].markdown(f"**{wd}**")

    for _week in range(6):
        row_cols = st.columns(7)
        placed_any = False
        for col_idx in range(7):
            cell_idx = _week * 7 + col_idx
            day = cell_idx - start_weekday + 1

            if day < 1 or day > days_in_month:
                row_cols[col_idx].empty()
                continue

            placed_any = True
            cell_date = date(month_base.year, month_base.month, day)
            key_date = _date_str(cell_date)

            has_entry = key_date in entries_by_date
            label = f"{day}"
            if has_entry:
                label += " •"

            if row_cols[col_idx].button(label, key=f"day_{key_date}"):
                st.session_state["journal_selected_date"] = cell_date
                st.session_state["journal_show_reflection"] = False
                st.rerun()

        if not placed_any:
            break

footer()

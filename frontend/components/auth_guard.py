import streamlit as st


def require_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.warning("Please log in to access this page (see the Auth page).")
        st.stop()

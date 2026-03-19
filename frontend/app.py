import streamlit as st
from components.sidebar import sidebar
from components.auth_guard import require_login

st.set_page_config(
    page_title="MedAssist",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

sidebar()

st.title("🧠 MedAssist")
st.markdown(
    """
    Welcome to **MedAssist**, your AI-powered mental health support assistant.

    Use the sidebar to:
    - log in or create an account
    - chat with the AI assistant
    - review your mental health records
    - track your recent status
    """
)

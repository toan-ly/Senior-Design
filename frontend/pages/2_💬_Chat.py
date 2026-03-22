import streamlit as st

from components.auth_guard import require_login
from components.footer import footer
from components.sidebar import sidebar
from utils.api import get_chat_history, send_chat_message

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

sidebar()
require_login()

st.title("Chat")
st.write("Welcome to the chat page!")


def _default_chat_messages():
    return [
        {
            "role": "assistant",
            "content": "Hello! I'm MedAssist. How are you feeling today?",
        }
    ]


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = _default_chat_messages()

# Load from Postgres if logged in with JWT but history not loaded yet
if (
    st.session_state.get("logged_in")
    and st.session_state.get("access_token")
    and not st.session_state.get("chat_history_loaded", False)
):
    username = st.session_state.get("username") or ""
    try:
        data = get_chat_history(
            session_id=username, access_token=st.session_state.access_token
        )
        msgs = data.get("messages") or []
        st.session_state.messages = (
            [{"role": m["role"], "content": m["content"]} for m in msgs]
            if msgs
            else _default_chat_messages()
        )
    except Exception:
        st.session_state.messages = _default_chat_messages()
    st.session_state.chat_history_loaded = True

# Show message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Type your message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            session_id = st.session_state.username or "guest"
            user_info = st.session_state.user_info or ""
            access_token = st.session_state.get("access_token")

            try:
                reply = send_chat_message(
                    session_id=session_id,
                    user_info=user_info,
                    message=prompt,
                    access_token=access_token,
                )
            except Exception as e:
                reply = f"Sorry, something went wrong: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

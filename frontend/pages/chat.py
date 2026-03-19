import streamlit as st

from components.auth_guard import require_login
from components.sidebar import sidebar
from utils.api import send_chat_message

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

sidebar()
require_login()

st.title("Chat")
st.write("Welcome to the chat page!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm MedAssist. How are you feeling today?",
        }
    ]

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

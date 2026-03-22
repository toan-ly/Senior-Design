import streamlit as st

from components.sidebar import sidebar
from components.footer import footer
from utils.api import get_chat_history, get_current_user, login_user, register_user


def _default_chat_messages():
    return [
        {
            "role": "assistant",
            "content": "Hello! I'm MedAssist. How are you feeling today?",
        }
    ]


def _load_chat_history_into_session(access_token: str, username: str) -> None:
    """Restore last conversation from Postgres for this account."""
    try:
        data = get_chat_history(session_id=username, access_token=access_token)
        msgs = data.get("messages") or []
        st.session_state.messages = (
            [{"role": m["role"], "content": m["content"]} for m in msgs]
            if msgs
            else _default_chat_messages()
        )
    except Exception:
        st.session_state.messages = _default_chat_messages()
    st.session_state.chat_history_loaded = True


st.set_page_config(page_title="Auth", page_icon="🔐", layout="centered")

sidebar()


def _init_session_state() -> None:
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("username", None)
    st.session_state.setdefault("user_info", None)
    st.session_state.setdefault("access_token", None)


_init_session_state()


st.title("Account")
st.caption(
    "Log in or create an account to use MedAssist. You can also continue as a guest."
)


login_tab, signup_tab, guest_tab = st.tabs(["Login", "Sign Up", "Guest"])


with login_tab:
    st.subheader("Login")
    username = st.text_input("Username", key="login_username").strip()
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", width="stretch", key="login_button"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            try:
                token_resp = login_user(username=username, password=password)
                access_token = token_resp["access_token"]
                user = get_current_user(access_token)

                st.session_state.access_token = access_token
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.user_info = (
                    f"username: {user['username']}, "
                    f"full_name: {user.get('full_name') or ''}, "
                    f"email: {user.get('email') or ''}"
                )
                _load_chat_history_into_session(access_token, user["username"])
                st.success(f"Welcome back, {user['username']}!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")


with signup_tab:
    st.subheader("Sign Up")
    su_username = st.text_input("Username", key="signup_username").strip()
    su_email = st.text_input("Email (optional)", key="signup_email").strip()
    su_full_name = st.text_input("Full name (optional)", key="signup_full_name").strip()
    su_password = st.text_input("Password", type="password", key="signup_password")
    su_password_confirm = st.text_input(
        "Confirm Password", type="password", key="signup_password_confirm"
    )

    if st.button("Create Account", width="stretch", key="signup_button"):
        if not su_username or not su_password:
            st.error("Username and password are required.")
        elif su_password != su_password_confirm:
            st.error("Passwords do not match.")
        elif len(su_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            try:
                register_user(
                    username=su_username,
                    password=su_password,
                    email=su_email or None,
                    full_name=su_full_name or None,
                )
                # Auto-login after successful registration
                token_resp = login_user(username=su_username, password=su_password)
                access_token = token_resp["access_token"]
                user = get_current_user(access_token)

                st.session_state.access_token = access_token
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.user_info = (
                    f"username: {user['username']}, "
                    f"full_name: {user.get('full_name') or ''}, "
                    f"email: {user.get('email') or ''}"
                )
                _load_chat_history_into_session(access_token, user["username"])
                st.success("Account created successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Sign up failed: {e}")


with guest_tab:
    st.subheader("Continue as Guest")
    st.markdown("Use the application without creating an account.")

    if st.button("Continue as Guest", width="stretch", key="guest_button"):
        st.session_state.logged_in = True
        st.session_state.username = "Guest"
        st.session_state.user_info = "username: Guest, information: not provided"
        st.session_state.access_token = None
        st.session_state.messages = _default_chat_messages()
        st.session_state.chat_history_loaded = True
        st.rerun()


footer()

import streamlit as st


def sidebar():
    with st.sidebar:
        st.image("frontend/assets/logo.svg")

        st.markdown("### How to use")
        st.markdown(
            """
            1. Log into your account  
            2. Open **Chat** and talk to MedAssist  
            3. MedAssist will assess your condition when enough information is collected  
            4. Review your history in **Health Tracker**
            """
        )

        st.divider()

        st.markdown("### Account")
        if st.session_state.get("logged_in", False):
            st.success(f"Logged in as **{st.session_state.get('username', 'User')}**")

            if st.button("Logout", width="stretch"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_info = None
                st.session_state.access_token = None
                st.rerun()
        else:
            st.warning("Not logged in")
            st.markdown(
                "Go to the **Auth** page to log in or create an account.",
            )

        st.divider()

import streamlit as st


def sidebar():
    with st.sidebar:
        st.image("frontend/assets/logo.svg")

        st.markdown("### How to use")
        st.markdown(
            """
            1. Log into your account  
            2. Open **Chat** and talk to the MedAssist chatbot
            3. MedAssist will generate an opinion of your condition when enough information has been collected
            4. Review your history in the **Health Tracker**
            5. Write personal journal entries in the **Journal**
            6. Visit other **Resources** for professional help
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

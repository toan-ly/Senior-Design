import streamlit as st


def footer() -> None:
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-size: 12px; color: #777; padding-bottom: 20px;">
        This site is for informational purposes only and does not provide licensed medical advice.
        If you are in immediate danger, call your local emergency number.
        <br/>© 2026 MedAssist. Icons and graphics are for demonstration purposes.
        </div>
        """,
        unsafe_allow_html=True,
    )

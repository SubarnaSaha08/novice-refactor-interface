import streamlit as st
from state.session import reset_session
from data.save_responses import save_user_responses


def show_completion():
    st.success("You have completed all problems. Click Submit to finish.")
    if st.button("Submit"):
        username = st.session_state.username
        responses = st.session_state.responses
        file_path = save_user_responses(responses, username)
        st.success(f"Responses submitted and saved to `{file_path}`.")
        reset_session()
        st.rerun()

import streamlit as st
from state.session import reset_session
from data.save_responses import autosave_user_responses


def show_completion():
    st.title("🎉 Survey Completed")
    st.success("You have completed all tasks!")

    username = st.session_state.username
    responses = st.session_state.responses

    # Save responses
    file_path = autosave_user_responses(responses, username)
    st.success(f"Responses saved to `{file_path}` ✅")

    # Show summary or download option (optional)
    with st.expander("View submitted responses"):
        st.write(responses)

    if st.button("🔁 Logout and Start Over"):
        reset_session()
        st.rerun()

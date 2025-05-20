import streamlit as st
from state.session import reset_session
from data.save_responses import autosave_user_responses


def show_completion():
    st.title("🎉 Survey Completed")
    st.success("You have completed all tasks!")

    username = st.session_state.get("username")
    responses = st.session_state.get("responses", {})

    if username is None or not responses:
        st.warning(
            "Looks like this page was opened without completing the survey first."
        )
        st.stop()

    # Save responses
    file_path = autosave_user_responses(responses, username, True)
    st.success(f"Responses saved to `{file_path}` ✅")

    # Show summary or download option (optional)
    with st.expander("View submitted responses"):
        st.write(responses)

    if st.button("🔁 Logout and Start Over"):
        reset_session()
        st.rerun()


def reset_session() -> None:
    # Copy keys to a list so we can delete safely while iterating
    for key in list(st.session_state.keys()):
        # Delete only the keys you actually want to clear
        del st.session_state[key]

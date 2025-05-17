import streamlit as st
from state.session import initialize_session
from components.login import login_form
from components.problem_display import handle_problem_display
from components.completion import show_completion
from config.settings import NUM_PROBLEMS


def main():
    st.title("Programming Problem Assessment")
    initialize_session()

    if not st.session_state.logged_in:
        login_form()
        return

    if st.session_state.problems_solved >= NUM_PROBLEMS:
        show_completion()
        return

    handle_problem_display()


if __name__ == "__main__":
    main()

import streamlit as st
from components.login import login
from components.task_selector import task_selector
from components.task_page import show_task_page
from components.completion import show_completion


def main():
    st.set_page_config(page_title="Programming Assessment", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        # login() returns True if login successful, then rerun to update UI
        if login():
            st.rerun()
    else:
        if st.session_state.page == "task_selector":
            task_selector()
        elif st.session_state.page == "task_page":
            show_task_page()
        elif st.session_state.page == "completion":
            show_completion()


if __name__ == "__main__":
    main()

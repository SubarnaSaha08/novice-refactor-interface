import streamlit as st
from data.loader import load_problems
from config.settings import CSV_PATH, NUM_PROBLEMS


def login_form():
    st.subheader("Login")
    username = st.text_input("Enter your username")
    if st.button("Login"):
        problems, user_found = load_problems(CSV_PATH, username.strip())
        if not user_found:
            st.error("Username not found. Try again.")
        else:
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.problems = problems[:NUM_PROBLEMS]
            st.success(f"Welcome, {st.session_state.username}!")
            st.rerun()

import streamlit as st
from data.loader import load_problems
from data.save_responses import load_user_responses_if_exists


def login():
    st.title("🔐 Survey Login")

    username = st.text_input("Enter your username")

    if st.button("Login"):
        if not username.strip():
            st.warning("Please enter your username.")
            return False  # Indicate login not successful
        
        if username == "admin244466666":
            st.session_state.logged_in = True
            st.session_state.page = "admin_page"
            return True
            
        problems, found = load_problems(username=username.strip())
        if not found:
            st.error("Username not found.")
            return False

        # Successful login
        st.session_state.logged_in = True
        st.session_state.username = username.strip()
        st.session_state.problems = problems[:3]
        st.session_state.current_index = 0
        st.session_state.problems_solved = 0

        # Load autosaved responses if any
        saved = load_user_responses_if_exists(username.strip())
        st.session_state.responses = saved if saved else {}

        st.success(f"Welcome, {username.strip()}!")

        # Instead of switch_page, set page state to move to task selector
        st.session_state.page = "task_selector"

        return True  # Indicate login successful

    return False

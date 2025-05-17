import streamlit as st


def initialize_session():
    for key, default in {
        "logged_in": False,
        "current_index": 0,
        "problems_solved": 0,
        "responses": {},
        "next_clicked": False,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_session():
    for key in [
        "logged_in",
        "current_index",
        "problems_solved",
        "responses",
        "next_clicked",
    ]:
        st.session_state[key] = (
            False
            if isinstance(st.session_state[key], bool)
            else 0 if isinstance(st.session_state[key], int) else {}
        )

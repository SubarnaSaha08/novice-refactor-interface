import streamlit as st
from components.shared_form import render_form
from components.utils import is_task_complete


def show_response_form_page():
    index = st.session_state.current_index
    problem = st.session_state.problems[index]
    response_key = f"response_{problem['id']}"
    response = st.session_state.responses.get(response_key, {})
    
    # Check completion properly
    if is_task_complete(response):
        st.success("✅ This task is complete!")
    else:
        st.warning("⚠️ Some fields are incomplete.")
        
    # st.subheader(f"Problem {index+1}: {problem['question']}")
    # st.code(problem["code"])
    
    st.header(f"Answer the questions for Problem {index+1}:")
    st.markdown("---")
    
    render_form(problem, response)

    if st.button("⬅️ Back to Task List"):
        st.session_state.page = "task_selector"
        st.rerun()

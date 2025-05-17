import streamlit as st
from components.utils import is_task_complete  # import the shared check function

def task_selector():
    st.title("Select a Task")

    task_statuses = []
    for i, problem in enumerate(st.session_state.problems):
        response_key = f"response_{problem['id']}"
        response_data = st.session_state.responses.get(response_key, {})

        if is_task_complete(response_data):
            status = "complete"
        elif len(response_data) > 0:
            status = "partial"
        else:
            status = "empty"

        task_statuses.append(status)

    # Display circular task buttons
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            label = f"{i+1}"
            status = task_statuses[i]

            color = {"complete": "green", "partial": "red", "empty": "lightgray"}[status]

            button_style = f"""
                <div style="text-align:center;">
                    <button style='border-radius:50%; width:60px; height:60px; background-color:{color}; font-size:20px; border:none;'>
                        {label}
                    </button>
                </div>
            """
            if st.button(f"Go to Task {i+1}", key=f"go_task_{i}"):
                st.session_state.current_index = i
                st.session_state.page = "task_page"
                st.rerun()
            st.markdown(button_style, unsafe_allow_html=True)

    # Completion condition
    if all(s == "complete" for s in task_statuses):
        st.markdown("---")
        if st.button("✅ Complete This Survey"):
            st.session_state.page = "completion"
            st.rerun()

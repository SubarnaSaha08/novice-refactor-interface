import streamlit as st
from data.save_responses import autosave_user_responses


def render_form(problem, response_data):
    pid = problem["id"]
    username = st.session_state.username

    # Ensure response dict for this problem id exists in session_state.responses
    response_key = f"response_{pid}"
    if response_key not in st.session_state.responses:
        st.session_state.responses[response_key] = {}
    # Use the session state dict as the response_data to keep it in sync
    response_data = st.session_state.responses[response_key]

    def field(key, label, options):
        full_key = f"{key}_{pid}"
        current_val = response_data.get(key)
        selected = st.radio(
            label,
            options,
            index=options.index(current_val) if current_val in options else 0,
            key=full_key,
        )
        if selected != current_val:
            response_data[key] = selected
            st.session_state.responses[response_key] = response_data
            autosave_user_responses(st.session_state.responses, username)

    # --- Section A: Code Comprehension Assessment ---
    st.markdown("---")
    st.subheader("**Section A: Code Comprehension Assessment**")
    st.write("Please answer the following questions regarding your understanding of the code:")

    field("difficulty", "How difficult do you find the problem?", [None, 1, 2, 3, 4, 5])
    field(
        "code_understanding",
        "How clearly do you understand the purpose of the given code?",
        [None, 1, 2, 3, 4, 5],
    )
    field(
        "logic_flow",
        "How well do you understand the flow of logic in the given code?",
        [None, 1, 2, 3, 4, 5],
    )
    field(
        "function_identification",
        "Can you identify key functions and their purposes?",
        [None, 1, 2, 3, 4, 5],
    )
    field("code_structure", "How well is the code structured?", [None, 1, 2, 3, 4, 5])

    for open_key, label in [
        ("open_ended_1", "Briefly describe what the code is doing:"),
        ("open_ended_2", "List any sections of the code that you find particularly confusing:"),
    ]:
        full_key = f"{open_key}_{pid}"
        val = st.text_area(label, key=full_key, value=response_data.get(open_key, ""))
        if val != response_data.get(open_key):
            response_data[open_key] = val
            st.session_state.responses[response_key] = response_data
            autosave_user_responses(st.session_state.responses, username)

    # --- Section B: Cognitive Load Assessment ---
    st.markdown("---")
    st.subheader("**Section B: Cognitive Load Assessment**")
    st.write("Rate your experience during the independent refactoring task (1 - Not at all, 5 - Extremely):")

    # NASA-TLX
    for metric in [
        "mental_demand",
        "physical_demand",
        "temporal_demand",
        "performance",
        "effort",
        "frustration",
    ]:
        field(metric, metric.replace("_", " ").title(), [None, 1, 2, 3, 4, 5])

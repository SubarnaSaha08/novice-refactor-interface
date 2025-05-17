import streamlit as st
from config.settings import NUM_PROBLEMS


def handle_problem_display():
    problems = st.session_state.problems
    index = st.session_state.current_index
    index = max(0, min(index, NUM_PROBLEMS - 1))
    st.session_state.current_index = index
    problem = problems[index]
    problem_number = index + 1

    display_problem(problem, problem_number)


def display_problem(problem, problem_number):
    # Show question and code
    st.subheader(f"Problem {problem_number}/{NUM_PROBLEMS}: {problem['question']}")
    st.code(problem["code"])

    # Unique key per problem
    key = f"response_{problem['id']}"
    if key not in st.session_state.responses:
        st.session_state.responses[key] = {
            "problem_id": problem["id"],
            "difficulty": None,
            "code_understanding": None,
            "logic_flow": None,
            "function_identification": None,
            "code_structure": None,
            "open_ended_1": None,
            "open_ended_2": None,
            "mental_demand": None,
            "physical_demand": None,
            "temporal_demand": None,
            "performance": None,
            "effort": None,
            "frustration": None,
        }

    data = st.session_state.responses[key]

    # Section A
    st.markdown("---")
    st.subheader("**Section A: Code Comprehension Assessment**")
    comprehension_fields = [
        (
            "difficulty",
            "How difficult do you find the problem? (1 - Very Easy, 5 - Very Hard)",
        ),
        (
            "code_understanding",
            "How clearly do you understand the purpose of the given code?",
        ),
        (
            "logic_flow",
            "How well do you understand the flow of logic in the given code?",
        ),
        (
            "function_identification",
            "Can you identify the key functions and their purposes in the code?",
        ),
        (
            "code_structure",
            "How well is the code structured for readability and maintainability?",
        ),
    ]
    for field, label in comprehension_fields:
        data[field] = st.radio(
            label,
            [None, 1, 2, 3, 4, 5],
            index=data[field] if data[field] is not None else 0,
            key=f"{field}_{problem['id']}",
        )

    data["open_ended_1"] = st.text_area(
        "Briefly describe what the code is doing:", key=f"open_ended_1_{problem['id']}"
    )
    data["open_ended_2"] = st.text_area(
        "List any sections of the code that you find particularly confusing:",
        key=f"open_ended_2_{problem['id']}",
    )

    # Section B
    st.markdown("---")
    st.subheader("**Section B: Cognitive Load Assessment (NASA-TLX)**")
    for field, label in [
        ("mental_demand", "Mental Demand"),
        ("physical_demand", "Physical Demand"),
        ("temporal_demand", "Temporal Demand"),
        ("performance", "Performance"),
        ("effort", "Effort"),
        ("frustration", "Frustration"),
    ]:
        data[field] = st.radio(
            label, [None, 1, 2, 3, 4, 5], key=f"{field}_{problem['id']}"
        )

    st.session_state.responses[key] = data
    if st.button("Next", disabled=not all(v is not None for v in data.values())):
        st.session_state.problems_solved += 1
        st.session_state.current_index += 1
        st.rerun()

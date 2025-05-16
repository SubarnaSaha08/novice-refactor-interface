import streamlit as st
import pandas as pd

# Load problems from CSV
def load_problems(csv_path, username):
    try:
        problems_df = pd.read_csv(csv_path)
        user_problems = problems_df[problems_df['user'] == username]
        if user_problems.empty:
            return [], False
        return user_problems.to_dict('records'), True
    except Exception as e:
        st.error(f"Error loading problems: {e}")
        return [], False

# Main function
def main():
    st.title("Programming Problem Assessment")

    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "problems_solved" not in st.session_state:
        st.session_state.problems_solved = 0
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "next_clicked" not in st.session_state:
        st.session_state.next_clicked = False

    # Login block
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Enter your username")
        if st.button("Login"):
            problems, user_found = load_problems("problems.csv", username.strip())
            if not user_found:
                st.error("Username not found. Try again.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.session_state.problems = problems[:3]
                st.success(f"Welcome, {st.session_state.username}!")
                st.rerun()
        return

    # Get user-specific problems
    problems = st.session_state.problems
    max_index = len(problems) - 1

    # Check if user has completed all problems
    if st.session_state.problems_solved >= 3:
        st.success("You have completed all problems. Click Submit to finish.")
        if st.button("Submit"):
            st.success("Your responses have been submitted successfully!")
            st.write(st.session_state.responses)  # Debug output
            # Reset state
            st.session_state.logged_in = False
            st.session_state.current_index = 0
            st.session_state.problems_solved = 0
            st.session_state.responses = {}
            st.session_state.next_clicked = False
            st.rerun()
        return

    # Ensure index is within bounds
    index = st.session_state.current_index
    index = max(0, min(index, max_index))
    st.session_state.current_index = index

    # Display problem number (1, 2, 3)
    problem_number = index + 1
    problem = problems[index]

    # Key for storing responses for this problem
    response_key = f"response_{problem['id']}"

    # Initialize response structure with `None`
    if response_key not in st.session_state.responses:
        st.session_state.responses[response_key] = {
            "problem_id": problem['id'],
            "difficulty": None,
            "code_understanding": None,
            "logic_flow": None,
            "function_identification": None,
            "code_structure": None,
            "open_ended_1": None,
            "open_ended_2": None
        }

    response_data = st.session_state.responses[response_key]

    # Display current problem
    st.subheader(f"Problem {problem_number}/3: {problem['question']}")
    st.code(problem['code'])

    # --- Survey Section Header ---
    st.markdown("---")
    st.subheader("**Section A: Code Comprehension Assessment**")
    st.write("Please answer the following questions regarding your understanding of the code:")


    # Difficulty Selection as Radio Button
    st.subheader("Survey Questions (1 - Low, 5 - High):")
    difficulty_options = [None, 1, 2, 3, 4, 5]
    difficulty_labels = ["Select", "1", "2", "3", "4", "5"]

    response_data["difficulty"] = st.radio(
        "How difficult do you find the problem?",
        options=difficulty_options,
        format_func=lambda x: difficulty_labels[difficulty_options.index(x)],
        index=difficulty_options.index(response_data["difficulty"]) if response_data["difficulty"] is not None else 0,
        key=f"difficulty_{problem['id']}"
    )

    response_data["code_understanding"] = st.radio(
        "Code Understanding: How clearly do you understand the purpose of the given code?",
        options=[None, 1, 2, 3, 4, 5],
        format_func=lambda x: "Select" if x is None else str(x),
        index=(response_data["code_understanding"] if response_data["code_understanding"] is not None else 0),
        key=f"code_understanding_{problem['id']}"
    )

    response_data["logic_flow"] = st.radio(
        "Logic Flow: How well do you understand the flow of logic in the given code?",
        options=[None, 1, 2, 3, 4, 5],
        format_func=lambda x: "Select" if x is None else str(x),
        index=(response_data["logic_flow"] if response_data["logic_flow"] is not None else 0),
        key=f"logic_flow_{problem['id']}"
    )

    response_data["function_identification"] = st.radio(
        "Function Identification: Can you identify the key functions and their purposes in the code?",
        options=[None, 1, 2, 3, 4, 5],
        format_func=lambda x: "Select" if x is None else str(x),
        index=(response_data["function_identification"] if response_data["function_identification"] is not None else 0),
        key=f"function_identification_{problem['id']}"
    )

    response_data["code_structure"] = st.radio(
        "Code Structure: How well is the code structured for readability and maintainability?",
        options=[None, 1, 2, 3, 4, 5],
        format_func=lambda x: "Select" if x is None else str(x),
        index=(response_data["code_structure"] if response_data["code_structure"] is not None else 0),
        key=f"code_structure_{problem['id']}"
    )

    response_data["open_ended_1"] = st.text_area(
        "Briefly describe what the code is doing:",
        key=f"open_ended_1_{problem['id']}",
        value=response_data["open_ended_1"] if response_data["open_ended_1"] else ""
    )

    response_data["open_ended_2"] = st.text_area(
        "List any sections of the code that you find particularly confusing:",
        key=f"open_ended_2_{problem['id']}",
        value=response_data["open_ended_2"] if response_data["open_ended_2"] else ""
    )

    # Update response data in session state
    st.session_state.responses[response_key] = response_data

    # Check if all required fields are filled
    all_fields_filled = (
        response_data["difficulty"] is not None and
        response_data["code_understanding"] is not None and
        response_data["logic_flow"] is not None and
        response_data["function_identification"] is not None and
        response_data["code_structure"] is not None and
        response_data["open_ended_1"] not in [None, ""] and
        response_data["open_ended_2"] not in [None, ""]
    )

    # Next Button
    next_disabled = not all_fields_filled

    # Handle Next button click
    next_clicked = st.button("Next", disabled=next_disabled)

    if next_clicked:
        # Reset the flag before rerun to ensure each click is registered
        st.session_state.next_clicked = False
        st.session_state.problems_solved += 1
        st.session_state.current_index += 1
        st.rerun()

if __name__ == "__main__":
    main()

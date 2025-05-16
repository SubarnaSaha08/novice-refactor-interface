import streamlit as st
import pandas as pd

# Load problems from CSV
def load_problems(csv_path):
    try:
        problems_df = pd.read_csv(csv_path)
        return problems_df.to_dict('records')
    except Exception as e:
        st.error(f"Error loading problems: {e}")
        return []

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

    # Login block
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Enter your username")
        if st.button("Login"):
            if username.strip():
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success(f"Welcome, {st.session_state.username}!")
            else:
                st.error("Username cannot be empty.")
        return

    # Load problems from CSV
    problems = load_problems("problems.csv")
    max_index = len(problems) - 1

    # Check if user has completed 3 problems
    if st.session_state.problems_solved >= 3:
        st.success("You have completed 3 problems. Logging out...")
        st.session_state.logged_in = False
        st.session_state.current_index = 0
        st.session_state.problems_solved = 0
        st.rerun()

    # Ensure index is within bounds
    index = st.session_state.current_index
    index = max(0, min(index, max_index))
    st.session_state.current_index = index

    # Display current problem
    problem = problems[index]
    st.subheader(f"Problem {problem['id']}: {problem['question']}")
    st.code(problem['code'])

    # Difficulty Rating
    difficulty = st.slider(
        f"Rate the difficulty of Problem {problem['id']} (1 - Very Easy, 5 - Very Hard)",
        1, 5, 3, key=f"difficulty_{problem['id']}"
    )

    # Feedback input
    feedback = st.text_area(f"Provide feedback for Problem {problem['id']}", key=f"feedback_{problem['id']}")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    # Previous button
    with col1:
        if st.button("Previous", disabled=(index == 0)):
            st.session_state.current_index -= 1

    # Next button
    with col2:
        if st.button("Next", disabled=(index == max_index)):
            # Increment problems solved only when moving forward
            st.session_state.problems_solved += 1
            st.session_state.current_index += 1

    # Logout button
    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_index = 0
            st.session_state.problems_solved = 0
            st.rerun()

if __name__ == "__main__":
    main()

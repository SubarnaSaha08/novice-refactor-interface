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
    if "difficulty_selected" not in st.session_state:
        st.session_state.difficulty_selected = None
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
            # Reset state
            st.session_state.logged_in = False
            st.session_state.current_index = 0
            st.session_state.problems_solved = 0
            st.session_state.difficulty_selected = None
            st.session_state.next_clicked = False
            st.rerun()
        return

    # Ensure index is within bounds
    index = st.session_state.current_index
    index = max(0, min(index, max_index))
    st.session_state.current_index = index

    # Display problem number (1, 2, 3)
    problem_number = index + 1

    # Display current problem
    problem = problems[index]
    st.subheader(f"Problem {problem_number}/3: {problem['question']}")
    st.code(problem['code'])

    # Difficulty Selection
    st.write("Select Difficulty (1 - Very Easy, 5 - Very Hard):")
    cols = st.columns(5)
    for i in range(1, 6):
        with cols[i - 1]:
            if st.button(str(i), key=f"difficulty_{problem['id']}_{i}"):
                st.session_state.difficulty_selected = i
                st.session_state.next_clicked = False  # Reset next click flag

    # Next Button Logic
    next_disabled = st.session_state.difficulty_selected is None

    # Handle Next button click
    next_clicked = st.button("Next", disabled=next_disabled)

    # Process Next button click
    if next_clicked and not st.session_state.next_clicked:
        # Mark as clicked to prevent double processing
        st.session_state.next_clicked = True

        # Proceed to the next problem
        st.session_state.problems_solved += 1
        st.session_state.current_index += 1

        # Reset difficulty selection for the next problem
        st.session_state.difficulty_selected = None

        # Trigger a rerun to reflect state updates immediately
        st.rerun()

if __name__ == "__main__":
    main()

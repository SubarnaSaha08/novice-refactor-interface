import pandas as pd
import streamlit as st


def load_problems(csv_path, username):
    try:
        problems_df = pd.read_csv(csv_path)
        user_problems = problems_df[problems_df["user"] == username]
        if user_problems.empty:
            return [], False
        return user_problems.to_dict("records"), True
    except Exception as e:
        st.error(f"Error loading problems: {e}")
        return [], False

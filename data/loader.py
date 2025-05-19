import pandas as pd

CSV_PATH = "assets/problems.csv"

def is_username_in_list(user_cell, username):
    if not user_cell:
        return False
    users = [u.strip() for u in user_cell.split(",") if u]
    return username in users

def load_problems(username, csv_path=CSV_PATH):
    try:
        df = pd.read_csv(csv_path)
        # Filter rows where username is in the comma-separated string
        user_df = df[df["user"].apply(is_username_in_list, args=(username,))]
        if user_df.empty:
            return [], False
        return user_df.to_dict("records"), True
    except Exception as e:
        print(f"Error loading problems: {e}")
        return [], False

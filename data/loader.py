import pandas as pd

CSV_PATH = "assets/problems.csv"


def load_problems(username, csv_path=CSV_PATH):
    try:
        df = pd.read_csv(csv_path)
        user_df = df[df["user"] == username]
        if user_df.empty:
            return [], False
        return user_df.to_dict("records"), True
    except Exception as e:
        print(f"Error loading problems: {e}")
        return [], False

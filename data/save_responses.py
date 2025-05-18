import os
import pandas as pd
from data.gdrive_uploader import upload_csv_to_gdrive

AUTOSAVE_DIR = "responses"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def autosave_user_responses(responses_dict, username):
    """Save each user's session response to a personal autosave file."""
    ensure_dir(AUTOSAVE_DIR)
    local_filepath = os.path.join(AUTOSAVE_DIR, f"{username}.csv")

    flattened = []
    for task_key, answers in responses_dict.items():
        row = {"username": username, "task_id": task_key}
        row.update(answers)
        flattened.append(row)

    df = pd.DataFrame(flattened)
    df.to_csv(local_filepath, index=False)

    csv_bytes = df.to_csv(index=False).encode()
    upload_csv_to_gdrive(
        csv_bytes, f"{username}_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"
    )
    return local_filepath


def load_user_responses_if_exists(username):
    filepath = os.path.join(AUTOSAVE_DIR, f"{username}.csv")
    if not os.path.exists(filepath):
        return None

    df = pd.read_csv(filepath)
    response_dict = {}
    for _, row in df.iterrows():
        task_id = row["task_id"]
        answer_data = row.drop(["username", "task_id"]).to_dict()
        response_dict[task_id] = answer_data
    return response_dict


def save_final_responses(responses_dict, username):
    """Append or overwrite the final shared CSV (one row per task)."""
    ensure_dir(os.path.dirname(FINAL_CSV) or ".")
    new_rows = []

    for task_key, answers in responses_dict.items():
        row = {"username": username, "task_id": task_key}
        row.update(answers)
        new_rows.append(row)

    new_df = pd.DataFrame(new_rows)

    if os.path.exists(FINAL_CSV):
        existing_df = pd.read_csv(FINAL_CSV)
        # Remove previous entries by this user (if resubmitting)
        existing_df = existing_df[existing_df["username"] != username]
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_csv(FINAL_CSV, index=False)

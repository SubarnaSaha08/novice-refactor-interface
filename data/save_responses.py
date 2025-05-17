import pandas as pd
import os
import uuid
from datetime import datetime


def save_user_responses(
    responses_dict, username, save_path="responses", master_file="all_responses.csv"
):
    os.makedirs(save_path, exist_ok=True)

    all_responses = []
    session_id = str(uuid.uuid4())  # Unique session ID

    for response in responses_dict.values():
        response_row = response.copy()
        response_row["username"] = username
        response_row["session_id"] = session_id
        response_row["timestamp"] = datetime.now().isoformat()
        all_responses.append(response_row)

    df = pd.DataFrame(all_responses)

    # Append to a master CSV
    full_path = os.path.join(save_path, master_file)
    if os.path.exists(full_path):
        df.to_csv(full_path, mode="a", header=False, index=False)
    else:
        df.to_csv(full_path, index=False)

    return full_path

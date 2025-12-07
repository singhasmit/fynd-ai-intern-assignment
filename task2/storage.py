import json
import os
from datetime import datetime

DATA_PATH = "data/submissions.json"


def _ensure_local_file():
    """Make sure data folder and JSON file exist."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)


def load_data():
    """Load all submissions from local JSON."""
    _ensure_local_file()
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_submission(submission):
    """Append one submission to local JSON."""
    data = load_data()
    data.append(submission)
    _ensure_local_file()
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def create_submission(rating, review, ai_response, ai_summary, ai_action):
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "rating": rating,
        "review": review,
        "ai_response": ai_response,
        "ai_summary": ai_summary,
        "ai_action": ai_action,
    }

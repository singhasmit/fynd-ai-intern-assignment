import json
import os
from datetime import datetime

DATA_PATH = "data/submissions.json"

def load_data():
    
    if not os.path.exists("data"):   #checking that data folder exists, if not making a new one
        os.makedirs("data")

    if not os.path.exists(DATA_PATH): #checking if json file exists , if not taking an empty list and saving the list
        with open(DATA_PATH, "w") as f:
            json.dump([], f)

    with open(DATA_PATH, "r") as f:    #loading the data
        return json.load(f)


def save_submission(submission):
    data = load_data()

    data.append(submission)

    with open (DATA_PATH, "w") as f:
        json.dump(data, f , indent=2)


def create_submission(rating , review , ai_response , ai_summary, ai_action):
    return{
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "rating": rating,
        "review": review,
        "ai_response": ai_response,
        "ai_summary": ai_summary,
        "ai_action": ai_action,
    }



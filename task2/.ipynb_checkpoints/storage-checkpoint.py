from datetime import datetime
from pymongo import MongoClient
import os

# ----------- MONGO SETUP -------------

MONGO_URI = "mongodb+srv://fynduser:Fynduser12345@cluster0.ba8j22x.mongodb.net/?appName=Cluster0"#os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set!")

client = MongoClient(MONGO_URI)
db = client["fynd_reviews"]          # database name
collection = db["submissions"]       # collection name


# ----------- SAVE SUBMISSION ----------
def save_submission(submission: dict):
    collection.insert_one(submission)


# ----------- LOAD SUBMISSIONS ----------
def load_data():
    all_docs = list(collection.find({}, {"_id": 0}))  # remove Mongo _id
    return all_docs


# ----------- CREATE SUBMISSION ----------
def create_submission(rating, review, ai_response, ai_summary, ai_action):
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "rating": rating,
        "review": review,
        "ai_response": ai_response,
        "ai_summary": ai_summary,
        "ai_action": ai_action,
    }

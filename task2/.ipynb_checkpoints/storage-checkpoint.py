import json
import os
from datetime import datetime
from pymongo import MongoClient

# Try to import Streamlit (only present in Streamlit apps)
try:
    import streamlit as st
except ImportError:
    st = None

DATA_PATH = "data/submissions.json"


def _get_mongo_collection():
    """Return a MongoDB collection object if MONGO_URI is configured,
    otherwise return None (we'll fall back to local JSON)."""

    # 1) Local dev: env var
    uri = os.getenv("MONGO_URI")

    # 2) Streamlit Cloud: secrets
    if not uri and st is not None:
        uri = st.secrets.get("MONGO_URI", "")

    if not uri:
        # No URI configured → no Mongo, we'll use local JSON instead
        if st:
            st.warning("MONGO_URI not set, using local JSON storage.")
        else:
            print("MONGO_URI not set, using local JSON storage.")
        return None

    try:
        client = MongoClient(uri)
        db = client["fynd_reviews"]
        return db["submissions"]
    except Exception as e:
        # If Mongo connection fails, also fall back to JSON
        if st:
            st.error(f"MongoDB connection failed: {e}. Falling back to local JSON.")
        else:
            print("MongoDB connection failed:", e)
        return None


COLLECTION = _get_mongo_collection()


def _ensure_local_file():
    """Ensure data folder and JSON file exist for local fallback."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)


def load_data():
    """Load all submissions from MongoDB if available, else from local JSON."""
    if COLLECTION is not None:
        docs = list(COLLECTION.find({}, {"_id": 0}))
        return docs

    # Fallback: local JSON
    _ensure_local_file()
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_submission(submission):
    """Save one submission to MongoDB if available, else append to local JSON."""
    if COLLECTION is not None:
        COLLECTION.insert_one(submission)
        return

    # Fallback: local JSON
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

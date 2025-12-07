from datetime import datetime
from pymongo import MongoClient
import os

# Try to import streamlit (only available in the apps, not in plain scripts)
try:
    import streamlit as st
except ImportError:
    st = None


def get_mongo_uri():
    # 1) Try environment variable (local dev)
    uri = os.getenv("MONGO_URI")

    # 2) If not set, try Streamlit secrets (Streamlit Cloud)
    if not uri and st is not None:
        uri = st.secrets.get("MONGO_URI")

    if not uri:
        raise ValueError("MONGO_URI not found in env vars or Streamlit secrets.")

    return uri


MONGO_URI = get_mongo_uri()

client = MongoClient(MONGO_URI)
db = client["fynd_reviews"]
collection = db["submissions"]

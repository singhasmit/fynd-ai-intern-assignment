import streamlit as st
import pandas as pd 

from storage import load_data

st.set_page_config(
    page_title = "Yelp Review Assistant-ADMIN",
    page_icon="📊",
    layout="wide",
)

st.title("Admin Dashboard – Review Monitor")
st.write("View user reviews, AI responses, and suggested actions.")

data = load_data()

if not data:
    st.info("No submissions yet. Submissions will be visible once the user submits any review")
else:
    df = pd.DataFrame(data)
    st.subheader("All Submissions")
    st.dataframe(df)

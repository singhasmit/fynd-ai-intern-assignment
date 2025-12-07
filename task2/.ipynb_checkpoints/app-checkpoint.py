import streamlit as st
import pandas as pd

from storage import load_data, save_submission, create_submission
from llm_client import generate_for_review   


st.set_page_config(
    page_title="Yelp Review Assistant",
    page_icon="⭐",
    layout="wide",
)

# Sidebar navigation
page = st.sidebar.radio(
    "Select dashboard:",
    ["User Dashboard", "Admin Dashboard"]
)

# ---------------- USER DASHBOARD ----------------
if page == "User Dashboard":
    st.title("Yelp Review Assistant – User Dashboard")
    st.write(
        "Share your experience by selecting a star rating and writing a short review."
    )

    rating = st.selectbox("Select a rating (1–5 stars):", [1, 2, 3, 4, 5])

    review = st.text_area(
        "Write your review here:",
        placeholder="Example: The food was great but the service was slow...",
    )

    if st.button("Submit review"):
        if not review.strip():
            st.error("Write a review first then click submit")
        else:
            # Calling llm
            ai_response, ai_summary, ai_action = generate_for_review(rating, review)

            # Creating and saving submisssion
            submission = create_submission(
                rating=rating,
                review=review,
                ai_response=ai_response,
                ai_summary=ai_summary,
                ai_action=ai_action,
            )
            save_submission(submission)

            st.success("Your review has been submitted!")
            st.subheader("AI Response")
            st.write(ai_response)


# ---------------- ADMIN DASHBOARD ----------------
elif page == "Admin Dashboard":
    st.title("Admin Dashboard – Review Monitor")
    st.write("View user reviews, AI responses, and suggested actions.")

    data = load_data()

    if not data:
        st.info("No submissions yet. Submissions will be visible once the user submits any review.")
    else:
        df = pd.DataFrame(data)
        st.subheader("All Submissions")
        st.dataframe(df)

import streamlit as st
from storage import save_submission , create_submission
from llm_client import generate_for_review


st.set_page_config(
    page_title="Yelp Review Assistant - User",
    page_icon="⭐",
    layout="centered",
)

st.title("Yelp Review Assistant – User Dashboard")
st.write(
    "Share your experience by selecting a star rating and writing a short review. "   
)

#page display
rating = st.selectbox("Select a rating (1–5 stars):", [1, 2, 3, 4, 5])

review = st.text_area(
    "Write your review here:",
    placeholder="Example: The food was great but the service was slow..."
)

if st.button("submit review"):  #if button is clicked then this block gets executed
    if not review.strip():          #review is empty
        st.error("Write a review first then click submit")
    else:
        # Calling LLM to generate AI response, summary, and action
        ai_response, ai_summary, ai_action = generate_for_review(rating, review)


        # Creating a submission dictionary to be saved in a json file
        submission = create_submission(
            rating=rating,
            review=review,
            ai_response=ai_response,
            ai_summary=ai_summary,
            ai_action=ai_action,
        )

        save_submission(submission)

       #showing success message after submission is successful
        st.success("Your review has been submitted!")
        st.subheader("AI Response (placeholder)")
        st.write(ai_response)
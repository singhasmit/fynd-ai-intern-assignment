import os
import json
import re
import google.generativeai as genai

try:
    import streamlit as st
except ImportError:
    st = None


def _get_api_key():
    """
    Try to get GEMINI_API_KEY from:
    1) Environment variable
    2) Streamlit secrets (when deployed)
    """
    key = os.getenv("GEMINI_API_KEY")

    if not key and st is not None:
        # Will work on Streamlit Cloud when you set secrets
        key = st.secrets.get("GEMINI_API_KEY")

    if not key:
        raise ValueError("GEMINI_API_KEY not found in env or Streamlit secrets.")

    return key


api_key = _get_api_key()
genai.configure(api_key=api_key)

from google.generativeai import GenerativeModel
model = GenerativeModel("gemini-2.0-flash")



def _parse_ai_json(text: str):
    """
    Try to extract ai_response, ai_summary, ai_action from model output.
    1) Try direct JSON
    2) Try extracting { ... } substring and parsing
    3) Fallback: treat whole text as ai_response
    """
    # --- 1. Direct JSON ---
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            ai_response = data.get("ai_response", "")
            ai_summary = data.get("ai_summary", "")
            ai_action = data.get("ai_action", "")
            return ai_response, ai_summary, ai_action, True
    except Exception:
        pass

    # --- 2. Extract JSON-like block with regex ---
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = match.group()
            data = json.loads(json_str)
            ai_response = data.get("ai_response", "")
            ai_summary = data.get("ai_summary", "")
            ai_action = data.get("ai_action", "")
            return ai_response, ai_summary, ai_action, True
    except Exception:
        pass

    # --- 3. Fallback: no JSON, just use raw text as response ---
    return text, "Summary not parsed.", "Action not parsed.", False


def generate_for_review(rating: int, review: str):
    """
    Given user rating + review, generate:
    - user-facing AI response
    - internal summary
    - recommended action
    """

    prompt = f"""
You are an assistant for a restaurant review dashboard.

The user gave this rating: {rating} star(s).
The user wrote this review:
\"\"\"{review}\"\"\"

Your job:

1. Write a short, empathetic reply to the user in natural language.
2. Summarize the main points of the review in 1–2 sentences for internal staff.
3. Suggest exactly ONE concrete action item for the restaurant team.

You MUST follow these rules:

- Respond with a SINGLE JSON object ONLY.
- Do NOT include ```json``` or any code fences.
- Do NOT include any extra text before or after the JSON.
- Use these EXACT keys:
  - "ai_response"
  - "ai_summary"
  - "ai_action"
- Use double quotes for all keys and string values.
- Make sure the JSON is valid.

Example of the format (this is just an example):

{{
  "ai_response": "Thank you for your feedback! We're glad you enjoyed the food and we will work on improving our service speed.",
  "ai_summary": "User liked the food but experienced slow service.",
  "ai_action": "Ask the floor manager to review staffing and service speed during peak hours."
}}

Now generate ONLY the JSON object for the given rating and review.
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    ai_response, ai_summary, ai_action, json_ok = _parse_ai_json(text)

    # Safety defaults if something is still missing
    if not ai_response:
        ai_response = "Thank you for your feedback!"

    if not ai_summary:
        ai_summary = "User shared feedback about their experience."

    if not ai_action:
        ai_action = "Review this feedback and decide if any follow-up is needed."

    return ai_response, ai_summary, ai_action

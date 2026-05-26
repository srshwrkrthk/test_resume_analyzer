from google import genai
import streamlit as st

from cache_utils import (
    get_cached_response,
    save_response_to_cache
)


def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


def generate_ai_insights(resume_text, role):
    cached = get_cached_response(resume_text + role)

    if cached:
        return cached

    api_key = get_api_key()

    if not api_key:
        raise Exception("GEMINI_API_KEY not found in Streamlit secrets.")

    client = genai.Client(
        api_key=api_key
    )

    limited_text = resume_text[:3000]

    prompt = f"""
    Give concise resume feedback for a {role} role.

    Resume:
    {limited_text}

    Provide:
    - Strengths
    - Missing Skills
    - Improvement Suggestions
    - Final Verdict

    Keep the response under 180 words.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        final_response = response.text

        save_response_to_cache(
            resume_text + role,
            final_response
        )

        return final_response

    except Exception as e:
        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            raise Exception("Gemini quota exhausted. Please try again later.")

        elif "API_KEY_INVALID" in error_message:
            raise Exception("Invalid Gemini API key.")

        elif "404" in error_message or "NOT_FOUND" in error_message:
            raise Exception("Gemini model not found. Check model name.")

        else:
            raise Exception(f"Gemini API error: {error_message}")
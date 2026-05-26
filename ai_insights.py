from dotenv import load_dotenv
import os
from google import genai

from cache_utils import (
    get_cached_response,
    save_response_to_cache
)

load_dotenv()
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def generate_ai_insights(
    resume_text,
    role
):

    cached = get_cached_response(
        resume_text + role
    )

    if cached:

        return cached

    prompt = f"""
    You are an expert ATS resume reviewer.

    Analyze this resume for the role of {role}.

    Resume Content:
    {resume_text}

    Give:
    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. ATS Improvement Suggestions
    5. Final Verdict

    Keep response professional and concise.
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

    except Exception:

        return """
AI insights temporarily unavailable.
Please try again later.
"""
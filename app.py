import streamlit as st
import pdfplumber

from skills import (
    software_engineer,
    data_science,
    cybersecurity
)

from analyzer import analyze_resume
from privacy import analyze_privacy


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Resume Intelligence Analyzer",
    layout="wide"
)

st.title("Resume Intelligence Analyzer")
st.write(
    "AI-Powered Resume Analysis and Privacy Risk Detection"
)


role = st.selectbox(

    "Select Target Role",

    [
        "Software Engineer",
        "Data Science",
        "Cybersecurity"
    ]
)


uploaded_file = st.file_uploader(

    "Upload Resume",

    type=["pdf"]
)



if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"


    if role == "Software Engineer":
        role_data = software_engineer

    elif role == "Data Science":
        role_data = data_science

    else:
        role_data = cybersecurity


    analysis_result = analyze_resume(
        text,
        role_data
    )

    privacy_result = analyze_privacy(text)


    st.subheader("Resume Match Score")

    st.metric(
        "Overall Match",
        f"{analysis_result['match_score']}%"
    )


    st.subheader("Privacy Risk Analysis")

    st.metric(
        "Privacy Risk Score",
        f"{privacy_result['privacy_score']}/100"
    )

    st.write(
        f"Risk Level: {privacy_result['risk_level']}"
    )



    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Mandatory Skills Found")

        st.write(
            analysis_result["mandatory_found"]
        )

        st.subheader("Preferred Skills Found")

        st.write(
            analysis_result["preferred_found"]
        )

    with col2:

        st.subheader("Missing Mandatory Skills")

        st.write(
            analysis_result["mandatory_missing"]
        )

        st.subheader("Missing Preferred Skills")

        st.write(
            analysis_result["preferred_missing"]
        )



    st.subheader("Bonus Skills Found")

    st.write(
        analysis_result["bonus_found"]
    )


    st.subheader("Sensitive Information Detected")

    st.write(
        {
            "Emails":
            privacy_result["emails"],

            "Phone Numbers":
            privacy_result["phone_numbers"],

            "LinkedIn":
            privacy_result["linkedin"],

            "GitHub":
            privacy_result["github"],

            "Aadhaar":
            privacy_result["aadhaar"],

            "PAN":
            privacy_result["pan"],

            "DOB":
            privacy_result["dob"]
        }
    )
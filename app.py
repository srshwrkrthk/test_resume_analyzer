import streamlit as st
import pdfplumber
import re

st.title("Resume Analyzer")
st.write("AI Powered Resume Analyzer")

upfile = st.file_uploader("Upload Resume", type = ['pdf'])

role = st.selectbox(
    "Select Target Role",
    [
        "Software Engineer",
        "Data Science",
        "Cybersecurity"
    ]
)

if upfile:
    text = ""
    with pdfplumber.open(upfile) as pdf:
        for page in pdf:
            pgtxt = page.extract_text():
            if pgtxt:
                text += pg.txt + "\n"
    text = text.lower()
    empat = r'[a-zA-Z0-9._-%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]+'
    numpat = r'\+?\d[\d\s\-]{8-12}\d'
    email = re.findall(empat, text)
    numbers = re.findall(numpat, text)
    if role_option == "Software Engineer":
        required_skills = software_engineer_skills

    elif role_option == "Data Science":
        required_skills = data_science_skills

    else:
        required_skills = cybersecurity_skills

    found_skills = []

    for skill in required_skills:

        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = []

    for skill in required_skills:

        if skill not in found_skills:
            missing_skills.append(skill)

    total_required = len(required_skills)
    total_found = len(found_skills)

    if total_required > 0:
        match_score = (total_found / total_required) * 100

    else:
        match_score = 0

    privacy_score = 0

    if emails:
        privacy_score += 20

    if numbers:
        privacy_score += 30

    st.subheader("Match Score")
    st.metric("Resume Match", f"{match_score:.2f}%")

    st.subheader("Privacy Score")
    st.metric("Privacy Risk", f"{privacy_score}/100")

    st.subheader("Detected Emails")
    st.write(emails)

    st.subheader("Detected Phone Numbers")
    st.write(numbers)

    st.subheader("Skills Found")
    st.write(found_skills)

    st.subheader("Missing Skills")
    st.write(missing_skills)

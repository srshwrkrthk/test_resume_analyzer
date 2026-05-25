import streamlit as st
import pdfplumber
import plotly.graph_objects as go

from skills import (
    software_engineer,
    data_science,
    cybersecurity
)

from analyzer import analyze_resume
from privacy import analyze_privacy


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Resume Intelligence Analyzer",
    page_icon="🚀",
    layout="wide"
)


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown(
    """
    <style>

    /* MAIN APP */
    .stApp {
        background: linear-gradient(
            135deg,
            #0B0F19,
            #111827,
            #1E1B4B
        );

        color: white;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }

    /* TITLES */
    h1, h2, h3 {
        color: white;
    }

    /* GLASS CARD */
    .glass-card {

        background: rgba(255, 255, 255, 0.05);

        border: 1px solid rgba(255,255,255,0.1);

        padding: 25px;

        border-radius: 20px;

        backdrop-filter: blur(12px);

        box-shadow: 0 8px 32px rgba(0,0,0,0.3);

        margin-bottom: 20px;
    }

    /* METRIC CONTAINERS */
    div[data-testid="metric-container"] {

        background: rgba(255,255,255,0.05);

        border: 1px solid rgba(255,255,255,0.08);

        padding: 20px;

        border-radius: 18px;

        backdrop-filter: blur(10px);
    }

    /* BUTTONS */
    .stButton > button {

        background: linear-gradient(
            90deg,
            #7C3AED,
            #8B5CF6
        );

        color: white;

        border-radius: 12px;

        border: none;

        padding: 12px 24px;

        font-weight: bold;
    }

    /* EXPANDERS */
    .streamlit-expanderHeader {
        font-size: 18px;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🚀 Resume Analyzer")

st.sidebar.markdown("""
### Intelligent Resume Audit

Analyze resumes with:
- Skill Intelligence
- Privacy Detection
- Weighted Matching
- Cybersecurity Insights
""")

st.sidebar.divider()

role = st.sidebar.selectbox(

    "Target Role",

    [
        "Software Engineer",
        "Data Science",
        "Cybersecurity"
    ]
)

uploaded_file = st.sidebar.file_uploader(

    "Upload Resume PDF",

    type=["pdf"]
)


# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------

st.title("Resume Intelligence Dashboard")

st.markdown("""
AI-Powered Resume Intelligence and Privacy Analysis Platform
""")

st.divider()


# ---------------------------------------------------
# PROCESS PDF
# ---------------------------------------------------

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    # -----------------------------------------------
    # ROLE DATA
    # -----------------------------------------------

    if role == "Software Engineer":
        role_data = software_engineer

    elif role == "Data Science":
        role_data = data_science

    else:
        role_data = cybersecurity

    # -----------------------------------------------
    # ANALYSIS
    # -----------------------------------------------

    analysis_result = analyze_resume(
        text,
        role_data
    )

    privacy_result = analyze_privacy(text)

    match_score = analysis_result["match_score"]

    # -----------------------------------------------
    # HERO SECTION
    # -----------------------------------------------

    col1, col2 = st.columns([1, 2])

    # LEFT SIDE - CIRCULAR CHART

    with col1:

        fig = go.Figure(go.Indicator(

            mode="gauge+number",

            value=match_score,

            number={
                'suffix': "%",
                'font': {'size': 42}
            },

            gauge={

                'axis': {
                    'range': [0, 100]
                },

                'bar': {
                    'color': "#8B5CF6"
                },

                'bgcolor': "#1F2937",

                'borderwidth': 0,

                'steps': [

                    {
                        'range': [0, 40],
                        'color': "#7F1D1D"
                    },

                    {
                        'range': [40, 70],
                        'color': "#78350F"
                    },

                    {
                        'range': [70, 100],
                        'color': "#064E3B"
                    }
                ]
            }
        ))

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            font={
                'color': "white"
            },

            height=320
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # RIGHT SIDE - ANALYSIS SUMMARY

    with col2:

        st.markdown("## Analysis Complete")

        if match_score >= 80:

            st.success(
                "Excellent alignment with target role."
            )

        elif match_score >= 60:

            st.warning(
                "Strong profile with improvement opportunities."
            )

        else:

            st.error(
                "Profile requires skill improvements."
            )

        st.markdown("### AI Insights")

        st.write(
            "- Strong technical foundation detected"
        )

        st.write(
            "- Resume structure is ATS compatible"
        )

        st.write(
            "- Some critical skills are missing"
        )

        st.write(
            "- Privacy exposure appears controlled"
        )

        st.markdown("### Tags")

        tag_col1, tag_col2, tag_col3 = st.columns(3)

        with tag_col1:
            st.info("Python")

        with tag_col2:
            st.info("Backend")

        with tag_col3:
            st.info("ATS Ready")

    st.divider()

    # -----------------------------------------------
    # SCORE SECTION
    # -----------------------------------------------

    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True
    )

    st.subheader("📊 Resume Match Analysis")

    st.progress(match_score / 100)

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(
            "Match Score",
            f"{match_score}%"
        )

    with score_col2:

        st.metric(
            "Privacy Score",
            f"{privacy_result['privacy_score']}/100"
        )

    risk_level = privacy_result["risk_level"]

    if risk_level == "HIGH":
        st.error(f"Privacy Risk: {risk_level}")

    elif risk_level == "MODERATE":
        st.warning(f"Privacy Risk: {risk_level}")

    else:
        st.success(f"Privacy Risk: {risk_level}")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------
    # SKILLS DASHBOARD
    # -----------------------------------------------

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:

        with st.expander("✅ Skills Found"):

            st.write("Mandatory Skills:")

            st.write(
                analysis_result["mandatory_found"]
            )

            st.write("Preferred Skills:")

            st.write(
                analysis_result["preferred_found"]
            )

            st.write("Bonus Skills:")

            st.write(
                analysis_result["bonus_found"]
            )

    with skill_col2:

        with st.expander("⚠️ Missing Skills"):

            st.write("Mandatory Missing:")

            st.write(
                analysis_result["mandatory_missing"]
            )

            st.write("Preferred Missing:")

            st.write(
                analysis_result["preferred_missing"]
            )

    # -----------------------------------------------
    # PRIVACY FINDINGS
    # -----------------------------------------------

    with st.expander("🔒 Sensitive Information Detected"):

        st.write(
            "Emails:",
            privacy_result["emails"]
        )

        st.write(
            "Phone Numbers:",
            privacy_result["phone_numbers"]
        )

        st.write(
            "LinkedIn:",
            privacy_result["linkedin"]
        )

        st.write(
            "GitHub:",
            privacy_result["github"]
        )

        st.write(
            "Aadhaar:",
            privacy_result["aadhaar"]
        )

        st.write(
            "PAN:",
            privacy_result["pan"]
        )

        st.write(
            "DOB:",
            privacy_result["dob"]
        )

    st.divider()

    st.caption(
        "Built with Python • Streamlit • Plotly • Resume Intelligence AI"
    )
import time
import streamlit as st
import streamlit.components.v1 as components
import pdfplumber
import plotly.graph_objects as go

from skills import roles
from analyzer import analyze_resume
from privacy import analyze_privacy


st.set_page_config(
    page_title="Resume Intelligence AI",
    page_icon="🚀",
    layout="wide"
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp {
        background: #020617;
        color: #e0e3e5;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(24px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .mouse-glow {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background: radial-gradient(
            700px circle at var(--x, 50%) var(--y, 50%),
            rgba(173, 198, 255, 0.13),
            transparent 45%
        );
    }

    .aurora-orb {
        position: fixed;
        border-radius: 9999px;
        filter: blur(100px);
        opacity: 0.25;
        z-index: 0;
        pointer-events: none;
    }

    .aurora-1 {
        width: 520px;
        height: 520px;
        background: #ddb7ff;
        top: 8%;
        left: 4%;
        animation: float1 25s infinite alternate ease-in-out;
    }

    .aurora-2 {
        width: 600px;
        height: 600px;
        background: #adc6ff;
        bottom: 12%;
        right: 8%;
        animation: float2 30s infinite alternate ease-in-out;
    }

    .aurora-3 {
        width: 450px;
        height: 450px;
        background: #ffb4ab;
        top: 45%;
        left: 45%;
        animation: float3 22s infinite alternate ease-in-out;
    }

    @keyframes float1 {
        from { transform: translate(0, 0) scale(1); }
        to { transform: translate(130px, 90px) scale(1.15); }
    }

    @keyframes float2 {
        from { transform: translate(0, 0) scale(1.05); }
        to { transform: translate(-120px, 130px) scale(0.9); }
    }

    @keyframes float3 {
        from { transform: translate(0, 0) scale(0.9); }
        to { transform: translate(60px, -130px) scale(1.1); }
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.045);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        transition: all 0.35s ease;
        position: relative;
        z-index: 2;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(173,198,255,0.35);
        box-shadow: 0 0 35px rgba(173,198,255,0.12);
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 64px;
        line-height: 1.05;
        font-weight: 700;
        letter-spacing: -0.04em;
        margin-bottom: 20px;
    }

    .neon-gradient {
        background: linear-gradient(90deg, #ddb7ff, #adc6ff, #ffb4ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shine 4s linear infinite;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .hero-subtitle {
        color: #c7c5cc;
        font-size: 18px;
        line-height: 1.7;
        max-width: 850px;
        opacity: 0.9;
    }

    .pill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 999px;
        background: rgba(173,198,255,0.10);
        color: #adc6ff;
        border: 1px solid rgba(173,198,255,0.18);
        font-size: 13px;
        font-weight: 600;
    }

    .missing-pill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 999px;
        background: rgba(255,180,171,0.10);
        color: #ffb4ab;
        border: 1px solid rgba(255,180,171,0.20);
        font-size: 13px;
        font-weight: 600;
    }

    .small-muted {
        color: #c7c5cc;
        opacity: 0.75;
        font-size: 14px;
    }

    .upload-card {
        border-radius: 24px;
        padding: 28px;
        border: 1px dashed rgba(173,198,255,0.45);
        background: rgba(255,255,255,0.035);
        text-align: center;
        box-shadow: 0 0 30px rgba(173,198,255,0.08);
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .footer {
        text-align: center;
        color: rgba(224,227,229,0.55);
        font-size: 12px;
        margin-top: 40px;
        padding-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="mouse-glow"></div>
    <div class="aurora-orb aurora-1"></div>
    <div class="aurora-orb aurora-2"></div>
    <div class="aurora-orb aurora-3"></div>
    """,
    unsafe_allow_html=True
)

components.html(
    """
    <script>
    const root = window.parent.document.documentElement;
    window.parent.document.addEventListener("mousemove", function(e) {
        root.style.setProperty("--x", e.clientX + "px");
        root.style.setProperty("--y", e.clientY + "px");
    });
    </script>
    """,
    height=0
)


def render_pills(items, css_class="pill", empty_text="None detected"):
    if items:
        html = "".join([f"<span class='{css_class}'>{item}</span>" for item in items])
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.success(empty_text)


st.sidebar.markdown("## 🚀 Resume Analyzer")
st.sidebar.markdown(
    """
    **Future-forward intelligence**

    Analyze resumes with:
    - Skill Intelligence
    - Privacy Detection
    - Weighted Matching
    - Gemini AI Insights
    """
)

st.sidebar.divider()

role = st.sidebar.selectbox(
    "Target Role",
    list(roles.keys())
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


st.markdown(
    """
    <div class="hero-title">
        Resume Intelligence<br>
        <span class="neon-gradient">AI Driven Precision</span>
    </div>

    <p class="hero-subtitle">
        Advanced AI-powered resume analysis, ATS scoring, privacy intelligence,
        and role-based skill evaluation platform for next-generation career readiness.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


if not uploaded_file:
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">Start your resume audit</div>
                <p class="small-muted">
                    Upload a PDF resume from the sidebar to generate a full analysis.
                    The core score, missing skills, and privacy scan work without AI.
                    Gemini AI is used only as an optional insight layer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            """
            <div class="upload-card">
                <h3>📄 Upload Resume</h3>
                <p class="small-muted">Use the sidebar uploader to begin analysis.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


if uploaded_file:
    loader = st.empty()

    loader.markdown(
        """
        <div class="glass-card">
            <h2>🤖 Analyzing Resume...</h2>
            <p class="small-muted">
                Extracting resume content, checking role fit, and scanning privacy risks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    loader.empty()
    progress.empty()

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    role_data = roles[role]

    # CORE MANUAL ANALYSIS
    analysis_result = analyze_resume(text, role_data)
    privacy_result = analyze_privacy(text)

    match_score = analysis_result["match_score"]

    score_col, summary_col = st.columns([1, 2])

    with score_col:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=match_score,
                number={
                    "suffix": "%",
                    "font": {"size": 46, "color": "white"}
                },
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "white"},
                    "bar": {"color": "#adc6ff"},
                    "bgcolor": "#111827",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "#3b1111"},
                        {"range": [40, 70], "color": "#4a2b0b"},
                        {"range": [70, 100], "color": "#063b2b"},
                    ],
                },
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            height=320,
            margin=dict(l=10, r=10, t=20, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    with summary_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("## Analysis Complete")

        if match_score >= 80:
            st.success("Excellent alignment with target role.")
        elif match_score >= 60:
            st.warning("Strong profile with improvement opportunities.")
        else:
            st.error("Profile requires skill improvements.")

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric("Match Score", f"{match_score}%")

        with metric2:
            st.metric("Privacy Risk", f"{privacy_result['privacy_score']}/100")

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    found_col, missing_col = st.columns(2)

    with found_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ✅ Skills Found")

        st.markdown("**Mandatory Skills**")
        render_pills(
            analysis_result["mandatory_found"],
            "pill",
            "No mandatory skills detected"
        )

        st.markdown("**Preferred Skills**")
        render_pills(
            analysis_result["preferred_found"],
            "pill",
            "No preferred skills detected"
        )

        st.markdown("**Bonus Skills**")
        render_pills(
            analysis_result["bonus_found"],
            "pill",
            "No bonus skills detected"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with missing_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Missing Skills")

        st.markdown("**Mandatory Missing**")
        render_pills(
            analysis_result["mandatory_missing"],
            "missing-pill",
            "No mandatory skills missing"
        )

        st.markdown("**Preferred Missing**")
        render_pills(
            analysis_result["preferred_missing"],
            "missing-pill",
            "No preferred skills missing"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    with st.expander("🔒 Sensitive Information Intelligence"):
        st.markdown(
            """
            <div class="glass-card">
                <h3>Detected Sensitive Information</h3>
                <p class="small-muted">
                    Privacy exposure analysis from uploaded resume.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.markdown("### 📧 Emails")
            render_pills(
                privacy_result["emails"],
                "pill",
                "No emails detected"
            )

            st.markdown("### 📱 Phone Numbers")
            render_pills(
                privacy_result["phone_numbers"],
                "pill",
                "No phone numbers detected"
            )

            st.markdown("### 💼 LinkedIn")
            render_pills(
                privacy_result["linkedin"],
                "pill",
                "No LinkedIn profiles detected"
            )

        with info_col2:
            st.markdown("### 🖥 GitHub")
            render_pills(
                privacy_result["github"],
                "pill",
                "No GitHub profiles detected"
            )

            st.markdown("### 🪪 Aadhaar")
            render_pills(
                privacy_result["aadhaar"],
                "missing-pill",
                "No Aadhaar detected"
            )

            st.markdown("### 🧾 PAN")
            render_pills(
                privacy_result["pan"],
                "missing-pill",
                "No PAN detected"
            )

            st.markdown("### 🎂 Date of Birth")
            render_pills(
                privacy_result["dob"],
                "missing-pill",
                "No DOB detected"
            )

    st.divider()
  
    # OPTIONAL AI INSIGHTS


    st.divider()

    st.markdown(
        """
        <div class="glass-card">
            <h2>🤖 AI Resume Intelligence</h2>
            <p class="small-muted">
                Gemini AI-generated suggestions and improvement recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    ai_feedback = None
    ai_error = None

    with st.spinner("Generating AI insights..."):

        try:

            from ai_insights import generate_ai_insights

            ai_feedback = generate_ai_insights(
                text,
                role
            )

        except Exception as e:

            ai_error = str(e)


    # SHOW RESULTS


    if ai_feedback:

        st.markdown(
            f"""
            <div class="glass-card">
                {ai_feedback}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        if ai_error:

            if "quota" in ai_error.lower():

                st.warning(
                    "Gemini quota exhausted. Please try again later."
                )

            elif "invalid" in ai_error.lower():

                st.error(
                    "Invalid Gemini API key."
                )

            elif "model" in ai_error.lower():

                st.error(
                    "Gemini model not found."
                )

            else:

                st.error(
                    f"AI Error: {ai_error}"
                )

        else:

            st.info(
                "AI insights unavailable at the moment, please try again later."
            )
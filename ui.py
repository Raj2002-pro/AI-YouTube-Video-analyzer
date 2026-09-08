import re
import streamlit as st
from YT_agent import build_youtube_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------- GLOBAL -------------------- */

    .stApp {
        background: #fafafa;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit default elements */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* -------------------- TOP NAVBAR -------------------- */

    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 4px 30px 4px;
        border-bottom: 1px solid #eeeeee;
        margin-bottom: 55px;
    }

    .brand {
        font-size: 22px;
        font-weight: 800;
        color: #202124;
        letter-spacing: -0.5px;
    }

    .brand-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: white;
        border-radius: 10px;
        margin-right: 9px;
        font-size: 16px;
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.25);
    }

    .nav-badge {
        background: #f3e8ff;
        color: #7c3aed;
        padding: 7px 13px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }


    /* -------------------- HERO -------------------- */

    .hero {
        text-align: center;
        margin-bottom: 42px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 30px;
        background: #f3e8ff;
        color: #7c3aed;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 52px;
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: -2px;
        color: #202124;
        margin: 0;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #a855f7,
            #6366f1
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        max-width: 700px;
        margin: 20px auto 0 auto;
        font-size: 18px;
        line-height: 1.6;
        color: #6b7280;
    }


    /* -------------------- FEATURE CARDS -------------------- */

    .features {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 38px;
        flex-wrap: wrap;
    }

    .feature {
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 12px 18px;
        color: #555555;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.025);
    }

    .feature.active {
        color: #7c3aed;
        border-color: #d8b4fe;
        background: #faf5ff;
    }


    /* -------------------- INPUT AREA -------------------- */

    .input-card {
        background: white;
        border: 1px solid #e9d5ff;
        border-radius: 18px;
        padding: 9px;
        box-shadow: 0 10px 35px rgba(124, 58, 237, 0.08);
        margin-bottom: 15px;
    }

    /* Streamlit text input */

    div[data-baseweb="input"] {
        border: none !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] > div {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    input {
        font-size: 16px !important;
    }

    /* Analyze button */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(
            135deg,
            #9333ea,
            #a855f7
        );
        color: white;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 7px 18px rgba(147, 51, 234, 0.25);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(147, 51, 234, 0.35);
    }


    /* -------------------- EXAMPLE -------------------- */

    .example-title {
        text-align: center;
        color: #888888;
        font-size: 13px;
        margin: 30px 0 12px 0;
    }

    .example-box {
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 14px;
        padding: 14px 18px;
        font-size: 14px;
        color: #555555;
        margin-bottom: 40px;
    }


    /* -------------------- LOADING -------------------- */

    .loading-box {
        text-align: center;
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 18px;
        padding: 30px;
        margin-top: 25px;
    }


    /* -------------------- RESULTS -------------------- */

    .results-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    .results-icon {
        width: 42px;
        height: 42px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #f3e8ff;
        border-radius: 12px;
        font-size: 21px;
    }

    .results-title {
        font-size: 25px;
        font-weight: 800;
        color: #202124;
    }

    .report-card {
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.035);
    }

    .report-card h1,
    .report-card h2,
    .report-card h3 {
        color: #202124;
    }

    .report-card h2 {
        margin-top: 30px;
        padding-bottom: 8px;
        border-bottom: 1px solid #eeeeee;
    }

    .report-card strong {
        color: #333333;
    }

    .report-card li {
        margin-bottom: 7px;
    }


    /* -------------------- FOOTER -------------------- */

    .footer {
        text-align: center;
        margin-top: 70px;
        padding-top: 25px;
        border-top: 1px solid #eeeeee;
        color: #999999;
        font-size: 13px;
    }

    .footer strong {
        color: #7c3aed;
    }


    /* -------------------- MOBILE -------------------- */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero h1 {
            font-size: 36px;
        }

        .hero-subtitle {
            font-size: 16px;
        }

        .navbar {
            margin-bottom: 35px;
        }

        .nav-badge {
            display: none;
        }

        .report-card {
            padding: 20px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    """
    <div class="navbar">

        <div class="brand">
            <span class="brand-icon">▶</span>
            AI YouTube Analyzer
        </div>

        <div class="nav-badge">
            ✨ Powered by AI
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ Intelligent Video Analysis
        </div>

        <h1>
            AI YouTube
            <span class="gradient-text">Video Analyzer</span>
        </h1>

        <div class="hero-subtitle">
            Turn any YouTube video into a clear, structured and
            intelligent analysis using AI.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    """
    <div class="features">

        <div class="feature active">
            ▶ YouTube
        </div>

        <div class="feature">
            📝 Summary
        </div>

        <div class="feature">
            💡 Key Insights
        </div>

        <div class="feature">
            🕐 Timeline
        </div>

        <div class="feature">
            🎯 Topics
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# URL INPUT
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns([4.5, 1.2], gap="small")

with col1:

    video_url = st.text_input(
        "YouTube URL",
        placeholder="🔗  Paste a YouTube URL here...",
        label_visibility="collapsed",
    )

with col2:

    analyze_button = st.button(
        "✨ Analyze",
        use_container_width=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# EXAMPLE
# ============================================================

example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

st.markdown(
    '<div class="example-title">Try an example</div>',
    unsafe_allow_html=True,
)

if st.button("▶ Try Example Video", use_container_width=False):

    st.session_state["example_url"] = example_url
    st.rerun()


if "example_url" in st.session_state:

    video_url = st.session_state["example_url"]

    st.markdown(
        f"""
        <div class="example-box">
            <strong>Example loaded:</strong><br>
            {video_url}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# URL VALIDATION
# ============================================================

def is_youtube_url(url):

    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"

    return re.match(pattern, url.strip()) is not None


# ============================================================
# ANALYZE VIDEO
# ============================================================

if analyze_button or "example_url" in st.session_state:

    if not video_url:

        st.warning("Please paste a YouTube video URL first.")

    elif not is_youtube_url(video_url):

        st.error("Please enter a valid YouTube URL.")

    else:

        # Remove example after analysis starts
        if "example_url" in st.session_state:
            del st.session_state["example_url"]

        with st.spinner("🧠 AI is analyzing your video..."):

            try:

                response = agent.run(
                    f"""
                    Analyze this YouTube video:

                    {video_url}
                    """
                )

                # ==================================================
                # RESULTS HEADER
                # ==================================================

                st.markdown(
                    """
                    <div class="results-header">

                        <div class="results-icon">
                            🧠
                        </div>

                        <div class="results-title">
                            AI Analysis Report
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ==================================================
                # RESULTS CARD
                # ==================================================

                st.markdown(
                    '<div class="report-card">',
                    unsafe_allow_html=True,
                )

                if hasattr(response, "content"):

                    st.markdown(response.content)

                else:

                    st.markdown(str(response))

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing the video."
                )

                with st.expander("Show technical error"):

                    st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        Built with <strong>Streamlit</strong> + 
        <strong>Agno</strong> + 
        <strong>Groq AI</strong>

        <br><br>

        AI YouTube Video Analyzer

    </div>
    """,
    unsafe_allow_html=True,
)

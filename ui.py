import re
from textwrap import dedent

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
    dedent(
        """
        <style>

        /* ==================================================
           GENERAL
        ================================================== */

        .stApp {
            background: #fafafa;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }


        /* ==================================================
           NAVBAR
        ================================================== */

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 4px 22px 4px;
            border-bottom: 1px solid #eeeeee;
            margin-bottom: 55px;
        }

        .brand {
            display: flex;
            align-items: center;
            font-size: 21px;
            font-weight: 800;
            color: #202124;
            letter-spacing: -0.5px;
        }

        .brand-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 35px;
            height: 35px;
            margin-right: 10px;
            border-radius: 10px;
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            color: white;
            font-size: 16px;
            box-shadow: 0 5px 15px rgba(124, 58, 237, 0.25);
        }

        .nav-badge {
            padding: 7px 14px;
            border-radius: 20px;
            background: #f3e8ff;
            color: #7c3aed;
            font-size: 13px;
            font-weight: 700;
        }


        /* ==================================================
           HERO
        ================================================== */

        .hero {
            text-align: center;
            margin-bottom: 38px;
        }

        .hero-badge {
            display: inline-block;
            padding: 7px 15px;
            margin-bottom: 20px;
            border-radius: 30px;
            background: #f3e8ff;
            color: #7c3aed;
            font-size: 13px;
            font-weight: 700;
        }

        .hero h1 {
            margin: 0;
            color: #202124;
            font-size: 52px;
            line-height: 1.12;
            font-weight: 800;
            letter-spacing: -2px;
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
            color: #6b7280;
            font-size: 18px;
            line-height: 1.6;
        }


        /* ==================================================
           FEATURE PILLS
        ================================================== */

        .features {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 32px;
        }

        .feature {
            padding: 11px 18px;
            border: 1px solid #eeeeee;
            border-radius: 12px;
            background: white;
            color: #555555;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.025);
        }

        .feature.active {
            border-color: #d8b4fe;
            background: #faf5ff;
            color: #7c3aed;
        }


        /* ==================================================
           INPUT AREA
        ================================================== */

        .input-wrapper {
            padding: 8px;
            border: 1px solid #e9d5ff;
            border-radius: 18px;
            background: white;
            box-shadow: 0 10px 35px rgba(124, 58, 237, 0.08);
            margin-bottom: 12px;
        }

        div[data-testid="stTextInput"] {
            margin-bottom: 0 !important;
        }

        div[data-testid="stTextInput"] label {
            display: none;
        }

        div[data-baseweb="input"] {
            border: none !important;
            background: transparent !important;
        }

        div[data-baseweb="input"] > div {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        div[data-baseweb="input"] input {
            font-size: 16px !important;
            color: #333333 !important;
        }


        /* ==================================================
           ANALYZE BUTTON
        ================================================== */

        .analyze-button button {
            min-height: 48px !important;
            border: none !important;
            border-radius: 12px !important;
            background: linear-gradient(
                135deg,
                #9333ea,
                #a855f7
            ) !important;
            color: white !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            box-shadow: 0 7px 18px rgba(147, 51, 234, 0.25);
            transition: all 0.2s ease;
        }

        .analyze-button button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(147, 51, 234, 0.35);
        }


        /* ==================================================
           EXAMPLE SECTION
        ================================================== */

        .example-title {
            text-align: center;
            margin-top: 27px;
            margin-bottom: 12px;
            color: #888888;
            font-size: 13px;
        }

        .example-divider {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 30px 0 20px 0;
            color: #999999;
            font-size: 13px;
        }

        .example-divider::before,
        .example-divider::after {
            content: "";
            height: 1px;
            flex: 1;
            background: #e9e9e9;
        }

        .example-url {
            padding: 15px 18px;
            border: 1px solid #eeeeee;
            border-radius: 14px;
            background: white;
            color: #555555;
            font-size: 14px;
        }


        /* ==================================================
           RESULTS HEADER
        ================================================== */

        .results-header {
            display: flex;
            align-items: center;
            gap: 13px;
            margin-top: 42px;
            margin-bottom: 20px;
        }

        .results-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 45px;
            height: 45px;
            border-radius: 13px;
            background: #f3e8ff;
            font-size: 22px;
        }

        .results-title {
            color: #202124;
            font-size: 26px;
            font-weight: 800;
        }


        /* ==================================================
           REPORT
        ================================================== */

        .report-card {
            padding: 30px;
            border: 1px solid #eeeeee;
            border-radius: 18px;
            background: white;
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.035);
        }

        .report-card h1,
        .report-card h2,
        .report-card h3 {
            color: #202124;
        }

        .report-card h2 {
            padding-bottom: 9px;
            margin-top: 30px;
            border-bottom: 1px solid #eeeeee;
        }

        .report-card strong {
            color: #333333;
        }

        .report-card li {
            margin-bottom: 7px;
        }


        /* ==================================================
           FOOTER
        ================================================== */

        .footer {
            padding-top: 25px;
            margin-top: 70px;
            border-top: 1px solid #eeeeee;
            text-align: center;
            color: #999999;
            font-size: 13px;
            line-height: 1.7;
        }

        .footer strong {
            color: #7c3aed;
        }


        /* ==================================================
           MOBILE
        ================================================== */

        @media (max-width: 700px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .navbar {
                margin-bottom: 35px;
            }

            .nav-badge {
                display: none;
            }

            .hero h1 {
                font-size: 36px;
                letter-spacing: -1px;
            }

            .hero-subtitle {
                font-size: 16px;
            }

            .feature {
                padding: 9px 13px;
                font-size: 13px;
            }

            .report-card {
                padding: 20px;
            }

        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# LOAD AI AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    dedent(
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
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    dedent(
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
                Turn any YouTube video into a clear, structured
                and intelligent analysis using AI.
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE PILLS
# ============================================================

st.markdown(
    dedent(
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
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# URL INPUT
# ============================================================

st.markdown(
    '<div class="input-wrapper">',
    unsafe_allow_html=True,
)

input_col, button_col = st.columns(
    [4.7, 1.3],
    gap="small",
)

with input_col:

    video_url = st.text_input(
        "YouTube URL",
        placeholder="🔗  Paste a YouTube URL here...",
        label_visibility="collapsed",
        key="video_url",
    )

with button_col:

    st.markdown(
        '<div class="analyze-button">',
        unsafe_allow_html=True,
    )

    analyze_button = st.button(
        "✨ Analyze",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# EXAMPLE VIDEO
# ============================================================

st.markdown(
    '<div class="example-title">Try an example</div>',
    unsafe_allow_html=True,
)

example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

example_button = st.button(
    "▶ Try Example Video"
)


# ============================================================
# DETERMINE WHICH URL TO ANALYZE
# ============================================================

if example_button:
    video_url = example_url
    analyze_button = True


# ============================================================
# YOUTUBE URL VALIDATION
# ============================================================

def is_youtube_url(url):

    if not url:
        return False

    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"

    return re.match(pattern, url.strip()) is not None


# ============================================================
# ANALYZE VIDEO
# ============================================================

if analyze_button:

    if not video_url:

        st.warning(
            "🔗 Please paste a YouTube video URL first."
        )

    elif not is_youtube_url(video_url):

        st.error(
            "❌ Please enter a valid YouTube URL."
        )

    else:

        with st.spinner(
            "🧠 AI is analyzing your video..."
        ):

            try:

                response = agent.run(
                    f"""
                    Analyze this YouTube video:

                    {video_url}
                    """
                )

                # --------------------------------------------
                # RESULTS HEADER
                # --------------------------------------------

                st.markdown(
                    dedent(
                        """
                        <div class="results-header">

                            <div class="results-icon">
                                🧠
                            </div>

                            <div class="results-title">
                                AI Analysis Report
                            </div>

                        </div>
                        """
                    ),
                    unsafe_allow_html=True,
                )

                # --------------------------------------------
                # REPORT CARD
                # --------------------------------------------

                st.markdown(
                    '<div class="report-card">',
                    unsafe_allow_html=True,
                )

                if hasattr(response, "content"):

                    st.markdown(
                        response.content
                    )

                else:

                    st.markdown(
                        str(response)
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

            except Exception as e:

                st.error(
                    "⚠️ Something went wrong while analyzing the video."
                )

                with st.expander(
                    "Show technical error"
                ):

                    st.code(
                        str(e)
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    dedent(
        """
        <div class="footer">

            Built with
            <strong>Streamlit</strong> +
            <strong>Agno</strong> +
            <strong>Groq AI</strong>

            <br>

            AI YouTube Video Analyzer

        </div>
        """
    ),
    unsafe_allow_html=True,
)

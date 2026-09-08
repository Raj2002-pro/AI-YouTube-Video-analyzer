import streamlit as st
from YT_agent import build_youtube_agent


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="▶️",
    layout="centered"
)


# ============================================================
# SIMPLE CSS
# ============================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background-color: #fafafa;
    }

    .block-container {
        max-width: 900px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Title */
    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        color: #222222;
        margin-bottom: 8px;
    }

    .purple {
        color: #8b3dff;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 35px;
    }

    /* Feature boxes */
    .feature-box {
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 13px 10px;
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #555555;
        margin-bottom: 25px;
    }

    .feature-active {
        border: 1px solid #c99cff;
        background: #f7efff;
        color: #7c2cff;
    }

    /* Input */
    div[data-testid="stTextInput"] input {
        height: 52px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        font-size: 15px;
        padding-left: 15px;
        background-color: white;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #9b4dff;
        box-shadow: 0 0 0 1px #9b4dff;
    }

    /* Analyze button */
    div.stButton > button {
        height: 52px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg, #8b3dff, #a855f7);
        color: white;
        font-size: 15px;
        font-weight: 700;
    }

    div.stButton > button:hover {
        border: none;
        color: white;
        background: linear-gradient(90deg, #7625e8, #9333ea);
    }

    /* Example section */
    .try-text {
        text-align: center;
        color: #999999;
        font-size: 13px;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    /* Results */
    .result-title {
        font-size: 28px;
        font-weight: 800;
        color: #222222;
        margin-top: 45px;
        margin-bottom: 20px;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #999999;
        font-size: 13px;
        margin-top: 60px;
    }

    /* Mobile */
    @media (max-width: 700px) {

        .main-title {
            font-size: 34px;
        }

        .subtitle {
            font-size: 16px;
        }

    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# AI AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<h1 class="main-title">AI YouTube <span class="purple">Video Analyzer</span></h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Turn any YouTube video into a clear, structured and intelligent analysis using AI.</p>',
    unsafe_allow_html=True
)


# ============================================================
# FEATURES
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        '<div class="feature-box feature-active">▶ YouTube</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="feature-box">📝 Summary</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="feature-box">💡 Key Insights</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="feature-box">🕐 Timeline</div>',
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        '<div class="feature-box">🎯 Topics</div>',
        unsafe_allow_html=True
    )


# ============================================================
# URL INPUT
# ============================================================

input_col, button_col = st.columns([4, 1])

with input_col:

    video_url = st.text_input(
        "YouTube URL",
        placeholder="🔗  Paste a YouTube URL here...",
        label_visibility="collapsed"
    )

with button_col:

    analyze_button = st.button(
        "✨ Analyze",
        use_container_width=True
    )


# ============================================================
# EXAMPLE
# ============================================================

st.markdown(
    '<div class="try-text">Try an example</div>',
    unsafe_allow_html=True
)

example_button = st.button(
    "▶ Try Example Video"
)


# Example YouTube video
example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

if example_button:
    video_url = example_url
    analyze_button = True


# ============================================================
# ANALYZE
# ============================================================

if analyze_button:

    if not video_url:

        st.warning("🔗 Please paste a YouTube video URL first.")

    elif "youtube.com" not in video_url and "youtu.be" not in video_url:

        st.error("❌ Please enter a valid YouTube URL.")

    else:

        with st.spinner("🧠 AI is analyzing the video..."):

            try:

                response = agent.run(
                    f"Analyze this YouTube video: {video_url}"
                )

                # --------------------------------------------
                # RESULT TITLE
                # --------------------------------------------

                st.markdown(
                    '<div class="result-title">🧠 AI Analysis Report</div>',
                    unsafe_allow_html=True
                )

                # --------------------------------------------
                # RESULT
                # --------------------------------------------

                if hasattr(response, "content"):

                    st.markdown(response.content)

                else:

                    st.markdown(str(response))

            except Exception as e:

                st.error(
                    "⚠️ Something went wrong while analyzing the video."
                )

                with st.expander("Show technical error"):

                    st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">Built with Streamlit • Agno • Groq AI</div>',
    unsafe_allow_html=True
)

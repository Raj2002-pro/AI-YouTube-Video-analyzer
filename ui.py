import streamlit as st
from YT_agent import build_youtube_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="▶️",
    layout="centered"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #fafafa;
}

.block-container {
    max-width: 900px;
    padding-top: 35px;
    padding-bottom: 50px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ================= TITLE ================= */

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

.subtitle {
    text-align: center;
    color: #666666;
    font-size: 18px;
    margin-bottom: 35px;
}


/* ================= FEATURE BUTTONS ================= */

div.stButton > button {
    border-radius: 12px;
    border: 1px solid #e5e5e5;
    background-color: white;
    color: #444444;
    font-size: 14px;
    font-weight: 600;
    min-height: 50px;
}

div.stButton > button:hover {
    border-color: #a855f7;
    color: #7c2cff;
}


/* ================= SELECTED MODE ================= */

.selected-mode {
    text-align: center;
    color: #7c2cff;
    font-size: 13px;
    font-weight: 600;
    margin-top: 4px;
    margin-bottom: 15px;
}


/* ================= INPUT ================= */

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


/* ================= ANALYZE ================= */

.analyze-container {
    margin-top: 0px;
}

.analyze-button button {
    height: 52px !important;
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(
        90deg,
        #8b3dff,
        #a855f7
    ) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}


/* ================= EXAMPLE ================= */

.try-text {
    text-align: center;
    color: #999999;
    font-size: 13px;
    margin-top: 25px;
    margin-bottom: 8px;
}


/* ================= RESULT ================= */

.result-title {
    font-size: 28px;
    font-weight: 800;
    color: #222222;
    margin-top: 45px;
    margin-bottom: 20px;
}

.summary-box {
    background: white;
    border: 1px solid #e7e7e7;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.03);
}

.summary-heading {
    font-size: 23px;
    font-weight: 800;
    color: #7c2cff;
    margin-bottom: 12px;
}


/* ================= FOOTER ================= */

.footer-text {
    text-align: center;
    color: #999999;
    font-size: 13px;
    margin-top: 60px;
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
# SESSION STATE
# ============================================================

if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = "YouTube"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<h1 class="main-title">AI YouTube <span class="purple">Video Analyzer</span></h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Turn any YouTube video into a clear, structured and intelligent analysis using AI.'
    '</p>',
    unsafe_allow_html=True
)


# ============================================================
# FEATURE BUTTONS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    if st.button("▶ YouTube", use_container_width=True):
        st.session_state.analysis_mode = "YouTube"


with col2:
    if st.button("📝 Summary", use_container_width=True):
        st.session_state.analysis_mode = "Summary"


with col3:
    if st.button("💡 Key Insights", use_container_width=True):
        st.session_state.analysis_mode = "Key Insights"


with col4:
    if st.button("🕐 Timeline", use_container_width=True):
        st.session_state.analysis_mode = "Timeline"


with col5:
    if st.button("🎯 Topics", use_container_width=True):
        st.session_state.analysis_mode = "Topics"


# ============================================================
# CURRENT MODE
# ============================================================

st.markdown(
    f'<div class="selected-mode">'
    f'Currently selected: {st.session_state.analysis_mode}'
    f'</div>',
    unsafe_allow_html=True
)


# ============================================================
# URL INPUT
# ============================================================

input_col, button_col = st.columns([4, 1])


with input_col:

    video_url = st.text_input(
        "YouTube URL",
        placeholder="🔗 Paste a YouTube URL here...",
        label_visibility="collapsed"
    )


with button_col:

    st.markdown(
        '<div class="analyze-container">',
        unsafe_allow_html=True
    )

    analyze_button = st.button(
        "✨ Analyze",
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
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

example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


if example_button:

    video_url = example_url
    analyze_button = True


# ============================================================
# PROMPTS FOR DIFFERENT BUTTONS
# ============================================================

mode_instructions = {

    "YouTube": """
Give a complete analysis of the YouTube video.

Cover:
- Video overview
- Detailed Summary
- Main ideas
- Important points
- Key insights
- Timeline
- Main topics
- Important conclusions

Make the explanation understandable to someone who has NOT watched
the video.
""",

    "Summary": """
Focus primarily on summarizing the video.

Give:
- A short summary
- A separate Detailed Summary section

The Detailed Summary must explain the complete discussion,
story, arguments, events and conclusions in enough detail that
someone who has never watched the video can understand the entire
idea of the video.

Do not just list keywords. Explain the ideas naturally.
""",

    "Key Insights": """
Focus primarily on the most important ideas and takeaways.

Give:
- Detailed Summary
- Key Insights
- Important arguments or observations
- Lessons / takeaways
- Important conclusions

The Detailed Summary must explain the complete video so that
a person who has never watched it can understand what was
discussed and why it matters.
""",

    "Timeline": """
Focus primarily on the chronological structure of the video.

Give:
- Detailed Summary
- Important timestamps
- What happens or is discussed at each major point
- Major transitions
- Important events or discussions in order

The Detailed Summary must still explain the complete idea of
the video for someone who has never watched it.
""",

    "Topics": """
Focus primarily on the major topics discussed in the video.

Give:
- Detailed Summary
- Main topics
- Subtopics
- What the speaker/guests say about each topic
- Important conclusions

The Detailed Summary must explain the complete video clearly
enough for someone who has never watched it.
"""
}


# ============================================================
# ANALYZE VIDEO
# ============================================================

if analyze_button:

    if not video_url:

        st.warning(
            "🔗 Please paste a YouTube video URL first."
        )

    elif (
        "youtube.com" not in video_url
        and
        "youtu.be" not in video_url
    ):

        st.error(
            "❌ Please enter a valid YouTube URL."
        )

    else:

        selected_mode = st.session_state.analysis_mode

        prompt = f"""
You are analyzing a YouTube video.

Video URL:
{video_url}

The user selected this analysis mode:
{selected_mode}

IMPORTANT:

Always include a clearly separated section called:

## 📖 Detailed Summary

This section is extremely important.

Explain the WHOLE video in a clear and comprehensive way.

Imagine the reader has NEVER watched this video.

After reading the Detailed Summary, they should understand:

- What the video is about
- Who is involved
- What is being discussed
- The important events or arguments
- How the discussion progresses
- Important examples mentioned
- Important opinions or viewpoints
- The final conclusion or outcome

Do not make the Detailed Summary just a collection of bullet points.

Explain the actual meaning and flow of the discussion in simple
language.

Do not invent information that is not present in the video.

After the Detailed Summary, provide the section requested
by the selected mode.

{mode_instructions[selected_mode]}

Use clear Markdown headings and bullet points where appropriate.
Keep the explanation detailed but easy to read.
"""

        # --------------------------------------------
        # RUN AGENT
        # --------------------------------------------

        with st.spinner(
            "🧠 AI is analyzing the video..."
        ):

            try:

                response = agent.run(prompt)

                # ----------------------------------------
                # RESULT TITLE
                # ----------------------------------------

                st.markdown(
                    '<div class="result-title">'
                    '🧠 AI Analysis Report'
                    '</div>',
                    unsafe_allow_html=True
                )

                # ----------------------------------------
                # RESULT
                # ----------------------------------------

                if hasattr(response, "content"):

                    report = response.content

                else:

                    report = str(response)

                st.markdown(report)

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
    '<div class="footer-text">'
    'Built with Streamlit • Agno • Groq AI'
    '</div>',
    unsafe_allow_html=True
)

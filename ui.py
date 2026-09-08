import os
import re
import streamlit as st

# ---------------------------------------------------------
# GROQ API KEY
# ---------------------------------------------------------
# This allows the app to work both locally (.env)
# and on Streamlit Cloud (Secrets).

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

from YT_agent import build_youtube_agent


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI YouTube Video Analyzer",
    page_icon="▶️",
    layout="wide",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: #ffffff;
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

    /* Main heading */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #292b38;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #a855f7,
            #c026d3
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666b78;
        margin-bottom: 35px;
    }

    /* Feature buttons */
    div.stButton > button {
        width: 100%;
        height: 62px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background: white;
        color: #30323d;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #a855f7;
        color: #7c3aed;
        transform: translateY(-1px);
    }

    /* Analyze button */
    .analyze-button button {
        background: linear-gradient(
            135deg,
            #8b3dff,
            #a855f7
        ) !important;

        color: white !important;
        border: none !important;
        font-weight: 700 !important;
    }

    .analyze-button button:hover {
        color: white !important;
        border: none !important;
    }

    /* URL input */
    div[data-testid="stTextInput"] input {
        height: 62px;
        border-radius: 15px;
        border: 1px solid #dedee5;
        font-size: 16px;
        padding-left: 20px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #9b5cff;
        box-shadow: 0 0 0 1px #9b5cff;
    }

    /* Report box */
    .report-title {
        font-size: 30px;
        font-weight: 800;
        color: #292b38;
        margin-top: 55px;
        margin-bottom: 25px;
    }

    .section-info {
        background: #faf7ff;
        border: 1px solid #eadcff;
        border-radius: 14px;
        padding: 15px 20px;
        margin-bottom: 25px;
        color: #6d28d9;
        font-size: 15px;
    }

    /* Example */
    .example-text {
        text-align: center;
        color: #888;
        margin-top: 35px;
        margin-bottom: 10px;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: #eeeeee;
        margin: 40px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# AGENT
# ---------------------------------------------------------
@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "analysis_report" not in st.session_state:
    st.session_state.analysis_report = None

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Detailed Summary"


# ---------------------------------------------------------
# FUNCTION TO EXTRACT SECTIONS
# ---------------------------------------------------------
def extract_section(report, section_name):
    """
    Extract one section from the AI-generated report.

    It looks for headings such as:
    ## Detailed Summary
    ## Key Insights
    ### Timeline
    etc.
    """

    if not report:
        return ""

    # Possible names for each section
    aliases = {
        "Detailed Summary": [
            "Detailed Summary",
            "Detailed summary",
            "Overall Summary",
            "Overall summary",
        ],

        "Summary": [
            "Summary",
            "Video Summary",
            "Brief Summary",
        ],

        "Key Insights": [
            "Key Insights",
            "Key insights",
            "Key Takeaways",
            "Key takeaways",
        ],

        "Timeline": [
            "Timeline",
            "Video Timeline",
            "Timestamps",
        ],

        "Topics": [
            "Topics",
            "Main Topics",
            "Topics Covered",
        ],
    }

    names = aliases.get(section_name, [section_name])

    # Build regex for headings
    heading_pattern = "|".join(
        re.escape(name) for name in names
    )

    # Look for markdown headings
    pattern = rf"(?im)^#+\s*({heading_pattern})\s*$"

    matches = list(re.finditer(pattern, report))

    if not matches:
        # If the section does not exist,
        # return a helpful message.
        return (
            f"### {section_name}\n\n"
            f"The AI report did not generate a separate "
            f"**{section_name}** section."
        )

    start = matches[0].start()

    # Find the next markdown heading
    next_heading = re.search(
        r"(?im)^#+\s+.+$",
        report[matches[0].end():]
    )

    if next_heading:
        end = matches[0].end() + next_heading.start()
    else:
        end = len(report)

    section = report[start:end].strip()

    # Remove the heading itself
    section = re.sub(
        rf"(?im)^#+\s*({heading_pattern})\s*$",
        "",
        section,
        count=1
    ).strip()

    return section


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-title">
        AI YouTube <span class="gradient-text">Video Analyzer</span>
    </div>

    <div class="subtitle">
        Turn any YouTube video into a clear, structured and intelligent
        analysis using AI.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# NAVIGATION BUTTONS
# ---------------------------------------------------------
st.markdown(
    "<div style='margin-top:10px;'></div>",
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5, col6 = st.columns(
    [1, 1, 1, 1, 1, 1]
)

with col1:
    if st.button("▶ YouTube"):
        st.session_state.selected_section = "Full Report"
        st.rerun()

with col2:
    if st.button("📑 Summary"):
        st.session_state.selected_section = "Summary"
        st.rerun()

with col3:
    if st.button("💡 Key Insights"):
        st.session_state.selected_section = "Key Insights"
        st.rerun()

with col4:
    if st.button("⏱️ Timeline"):
        st.session_state.selected_section = "Timeline"
        st.rerun()

with col5:
    if st.button("🎯 Topics"):
        st.session_state.selected_section = "Topics"
        st.rerun()

with col6:
    if st.button("📖 Detailed Summary"):
        st.session_state.selected_section = "Detailed Summary"
        st.rerun()


# ---------------------------------------------------------
# URL INPUT
# ---------------------------------------------------------
st.markdown(
    "<div style='margin-top:30px;'></div>",
    unsafe_allow_html=True
)

input_col, button_col = st.columns([4, 1])

with input_col:
    video_url = st.text_input(
        "YouTube URL",
        placeholder="Paste a YouTube URL here...",
        label_visibility="collapsed",
    )

with button_col:
    st.markdown(
        '<div class="analyze-button">',
        unsafe_allow_html=True
    )

    analyze = st.button(
        "✨ Analyze",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# EXAMPLE
# ---------------------------------------------------------
st.markdown(
    "<div class='example-text'>Try an example</div>",
    unsafe_allow_html=True
)

example_col1, example_col2, example_col3 = st.columns(
    [1, 2, 1]
)

with example_col1:
    if st.button("▶ Try Example Video"):
        video_url = (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        analyze = True


# ---------------------------------------------------------
# ANALYZE VIDEO
# ---------------------------------------------------------
if analyze:

    if not video_url.strip():
        st.warning("Please enter a YouTube video URL.")

    else:

        with st.spinner(
            "🎬 Analyzing the video... This may take a moment."
        ):

            try:

                response = agent.run(
                    f"""
                    Analyze this YouTube video:

                    {video_url}

                    Provide a complete structured report.
                    Make sure the report contains these sections:

                    ## Detailed Summary
                    Explain the complete idea of the video in detail.
                    A person who has NOT watched the video should be
                    able to understand the entire video from this section.

                    ## Summary
                    Give a shorter overview of the video.

                    ## Key Insights
                    List the most important ideas, lessons,
                    arguments and takeaways.

                    ## Timeline
                    Give important timestamps and explain what
                    happens at those points.

                    ## Topics
                    List the major topics discussed in the video.

                    ## Video Overview
                    Include title, channel, approximate duration,
                    format and other useful information.
                    """
                )

                st.session_state.analysis_report = response.content

                # Automatically open Detailed Summary
                st.session_state.selected_section = "Detailed Summary"

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing the video."
                )

                st.exception(e)


# ---------------------------------------------------------
# DISPLAY REPORT
# ---------------------------------------------------------
if st.session_state.analysis_report:

    report = st.session_state.analysis_report
    selected = st.session_state.selected_section

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🧠 AI Analysis Report",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # FULL REPORT
    # -----------------------------------------------------
    if selected == "Full Report":

        st.markdown(
            """
            <div class="section-info">
                📚 Showing the complete AI analysis report.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(report)

    # -----------------------------------------------------
    # INDIVIDUAL SECTION
    # -----------------------------------------------------
    else:

        st.markdown(
            f"""
            <div class="section-info">
                📌 Currently viewing: <strong>{selected}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        section_content = extract_section(
            report,
            selected
        )

        st.markdown(section_content)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="divider"></div>

    <div style="
        text-align:center;
        color:#999;
        font-size:14px;
        padding-bottom:20px;
    ">
        🤖 Powered by AI • YouTube Video Analyzer
    </div>
    """,
    unsafe_allow_html=True
)

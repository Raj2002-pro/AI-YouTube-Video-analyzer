#lec-->deployment
#so this file is created to access the yt analyser for deployment using streamlit
import streamlit as st
from YT_agent import build_youtube_agent #we are importing the build_youtube_agent function from the YT_agent.py file to access the youtube agent

#you can explore streamlit documentation to know more about it https://docs.streamlit.io/get-started/fundamentals/main-concepts

st.set_page_config(
    page_title="YouTube Video Analyzer",
    layout="centered",


)

st.title("▶AI YouTube Video Analyzer")#shows the title of the app on the web page

#here we are caching the youtube agent to store the frequently used data into a small temporary memory called cache so that 
# it can be accessed quickly and easily without having to re-run the code again and again
#all the main data stored in main memory and it takes time to access it but if we store the frequently used data in cache then 
# it can be accessed quickly and easily without having to re-run the code again and again
#so we add the function get_agent() to cache the youtube agent so that it can be accessed quickly and easily without having to re-run the code again and again
#watch more about this on  https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource
@st.cache_resource
def get_agent():
    return build_youtube_agent() #this function will return the youtube agent created in the YT_agent.py file

agent=get_agent() #this will call the get_agent function to get the youtube agent

#we are doing this becaz each time the web fresh is refreshed the agent will not be created from scratch again and again and it will use the same agent for all the queries

#input box
video_url=st.text_input("enter youtube video url")  #this shows the input space where the link is pasted and it is stored in the form of string

button =st.button("analyze video")#creating the button #this button in stored as True/False  ..if we click the button then its true and otherwise its false

if video_url and button:# whenever there is input string or video link availabe and button is clicked then it will work
    with st.spinner("Analyzing video..."):#the agent takes some time to analyze the whole thing so during that it is shown 
        response = agent.run(
            f"Analyze this video:{video_url}"

        )
        st.markdown("Analysis report of videos:")
        st.markdown(response.content)#a huge text comes as a response or output but we just want to show the content part





import streamlit as st

from utils.theme import load_css


load_css()


st.title(
"AI Resume Builder"
)
import streamlit as st

from utils.ui_components import (
    show_logo,
    hero_section,
    feature_card
)



st.set_page_config(

page_title="AI Resume Builder",

page_icon="🚀",

layout="wide"

)



show_logo()



hero_section(

"resume_hero.png",

"AI Resume Builder 🚀",

"Create ATS friendly professional resumes with AI assistance, smart templates and resume scoring."

)



st.divider()



st.subheader(

"Powerful Features"

)



col1,col2,col3 = st.columns(3)



with col1:

    feature_card(

    "ATS Score",

    "Check resume compatibility before applying",

    "ats_score.png"

    )



with col2:


    feature_card(

    "AI Optimization",

    "Improve resume content automatically",

    "ai_robot.png"

    )



with col3:


    feature_card(

    "Professional Templates",

    "Download DOCX and PDF resumes",

    "download.png"

    )



st.divider()



st.page_link(

"pages/1_Create_Resume.py",

label="📝 Create Resume"

)



st.page_link(

"pages/2_Upload_Resume.py",

label="📂 Upload Resume"

)



st.page_link(

"pages/4_Download.py",

label="⬇ Download Resume"

)
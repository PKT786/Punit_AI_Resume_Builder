import streamlit as st


st.title(
"🚀 AI Resume Builder"
)


st.write(
"""
Create ATS-friendly professional resumes
using AI and smart templates.
"""
)



st.page_link(

"pages/1_Create_Resume.py",

label="✍️ Create New Resume"

)



st.page_link(

"pages/2_Upload_Resume.py",

label="📂 Upload Existing Resume"

)



st.page_link(

"pages/3_ATS_Checker.py",

label="📊 Check ATS Score"

)



st.page_link(

"pages/4_Download.py",

label="⬇️ Download Resume"

)
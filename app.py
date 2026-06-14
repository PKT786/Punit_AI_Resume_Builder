import streamlit as st

from components.header import hero
from components.cards import feature_cards


st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)


# ----------------------------
# Custom CSS Premium UI
# ----------------------------

st.markdown(
"""
<style>

.main-title {

font-size:55px;
font-weight:800;
color:#1f2937;

}


.subtitle {

font-size:22px;
color:#6b7280;

}


.stButton button {

height:55px;
width:100%;

border-radius:12px;

font-size:18px;

font-weight:600;

background:
linear-gradient(
90deg,
#6366f1,
#06b6d4
);

color:white;

border:none;

}


</style>

""",
unsafe_allow_html=True
)



# ----------------------------
# Hero Section
# ----------------------------

hero()



st.markdown(
"""
<div class="subtitle">

Create recruiter-ready ATS resumes using Artificial Intelligence.
Upload your resume, optimize content, check ATS score and download PDF/DOCX.

</div>

""",
unsafe_allow_html=True
)



st.write("")



# ----------------------------
# Action Buttons
# ----------------------------


col1,col2 = st.columns(2)



with col1:


    if st.button(
        "🚀 Create New Resume"
    ):


        st.switch_page(
            "pages/1_Create_Resume.py"
        )




with col2:


    if st.button(
        "📤 Upload Existing Resume"
    ):


        st.switch_page(
            "pages/2_Upload_Resume.py"
        )



st.write("")



# ----------------------------
# Features
# ----------------------------


st.subheader(
"Why Use AI Resume Builder?"
)


feature_cards()



# ----------------------------
# Statistics
# ----------------------------


st.write("")


c1,c2,c3,c4 = st.columns(4)



c1.metric(
"AI Optimization",
"100%"
)


c2.metric(
"ATS Friendly",
"90+ Score"
)


c3.metric(
"Templates",
"3+"
)


c4.metric(
"Export",
"PDF/DOCX"
)        

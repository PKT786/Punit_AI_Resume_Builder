import streamlit as st

from utils.theme import load_css


load_css()


st.title(
"AI Resume Builder"
)
import streamlit as st
from utils.ui_components import hero_section

hero_section(

"resume_hero.png",

"Create Your Resume",

"Build a professional ATS-ready resume in minutes"

)

st.set_page_config(

    page_title="Create Resume",

    page_icon="📝",

    layout="wide"

)



st.title(
"📝 Create New Resume"
)



st.write(

"""
Fill your details and generate an ATS-friendly resume.
"""

)



# ------------------------
# User Inputs
# ------------------------


name = st.text_input(

"Full Name"

)



email = st.text_input(

"Email"

)



phone = st.text_input(

"Phone Number"

)



location = st.text_input(

"Location"

)



role = st.text_input(

"Job Role / Title"

)



summary = st.text_area(

"Professional Summary"

)



skills = st.text_area(

"Skills (comma separated)"

)



experience = st.text_area(

"Work Experience"

)



education = st.text_area(

"Education"

)




# ------------------------
# Create Resume Object
# ------------------------


if st.button(

"Generate Resume"

):


    resume_data = {


        "name": name,


        "email": email,


        "phone": phone,


        "location": location,


        "headline": role,


        "job_title": role,


        "summary": summary,


        "skills": skills.split(","),


        "experience": [

            experience

        ],


        "education": [

            education

        ]


    }



    # Save for Download page


    st.session_state["resume"] = resume_data



    st.success(

    "Resume information saved successfully ✅"

    )



    st.info(

    "Now go to Download Resume page"

    )
import streamlit as st
import os


st.set_page_config(

    page_title="Create Resume",

    page_icon="📝",

    layout="wide"

)


from utils.theme import load_css

load_css()



# -------------------------
# Hero
# -------------------------

hero="assets/resume_hero.png"


if os.path.exists(hero):

    st.image(

        hero,

        use_container_width=True

    )




st.title(
    "📝 Create Resume"
)


st.write(

"Create a professional ATS friendly resume by entering your details."

)



st.divider()





# -------------------------
# Basic Details
# -------------------------


st.subheader(

"Personal Information"

)



col1,col2=st.columns(2)



with col1:


    name=st.text_input(

        "Full Name"

    )


    email=st.text_input(

        "Email"

    )


    phone=st.text_input(

        "Phone"

    )



with col2:


    location=st.text_input(

        "Location"

    )


    linkedin=st.text_input(

        "LinkedIn URL"

    )


    github=st.text_input(

        "Github URL"

    )





# -------------------------
# Career
# -------------------------


st.subheader(

"Professional Details"

)



job_title=st.text_input(

    "Job Title"

)



summary=st.text_area(

    "Professional Summary"

)



skills=st.text_area(

    "Skills (comma separated)"

)





# -------------------------
# Experience
# -------------------------


st.subheader(

"Experience"

)


company=st.text_input(

    "Company Name"

)


role=st.text_input(

    "Role"

)


duration=st.text_input(

    "Duration"

)



responsibilities=st.text_area(

    "Responsibilities (one per line)"

)





# -------------------------
# Education
# -------------------------


st.subheader(

"Education"

)


degree=st.text_input(

    "Degree"

)


university=st.text_input(

    "University"

)


year=st.text_input(

    "Year"

)






# -------------------------
# Projects
# -------------------------


st.subheader(

"Projects"

)


project_name=st.text_input(

    "Project Name"

)


project_description=st.text_area(

    "Project Description"

)







# -------------------------
# Generate JSON
# -------------------------


if st.button(

    "Generate Resume"

):


    resume_data={


        "name":name,


        "email":email,


        "phone":phone,


        "location":location,


        "linkedin":linkedin,


        "github":github,


        "job_title":job_title,


        "summary":summary,



        "skills":[

            x.strip()

            for x in skills.split(",")

            if x.strip()

        ],



        "experience":[

            {

            "company":company,

            "role":role,

            "duration":duration,


            "responsibilities":[

                x

                for x in responsibilities.split("\n")

                if x.strip()

            ]

            }

        ],



        "education":[


            {

            "degree":degree,

            "university":university,

            "year":year

            }

        ],



        "projects":[


            {

            "name":project_name,

            "description":project_description,

            "link":""

            }

        ],



        "certifications":[],

        "achievements":[]

    }




    st.session_state["resume_data"]=resume_data



    st.success(

        "Resume data created successfully"

    )



    st.switch_page(

        "pages/4_Download.py"

    )

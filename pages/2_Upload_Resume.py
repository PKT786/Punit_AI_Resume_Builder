import streamlit as st
import os


# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(

    page_title="Upload Resume",

    page_icon="📄",

    layout="wide"

)



# -------------------------------
# Theme CSS
# -------------------------------

from utils.theme import load_css

load_css()



# -------------------------------
# Imports
# -------------------------------

from utils.resume_parser import (

    extract_resume_text,

    parse_resume

)


from ai.resume_optimizer import optimize_resume





# -------------------------------
# Hero Section
# -------------------------------

hero_path = "assets/resume_hero.png"


if os.path.exists(hero_path):


    st.image(

        hero_path,

        use_container_width=True

    )



st.markdown(

"""
# 📄 AI Resume Builder

Upload your existing resume and generate a professional ATS optimized resume.

Features:

✅ Resume parsing  
✅ AI improvement  
✅ ATS scoring  
✅ Premium templates  
✅ DOCX/PDF download

"""

)



st.divider()





# -------------------------------
# Upload Resume
# -------------------------------


uploaded_file = st.file_uploader(

    "Upload your Resume (DOCX)",

    type=[

        "docx"

    ]

)





if uploaded_file:



    with st.spinner(

        "Reading resume..."

    ):



        # Extract text


        resume_text = extract_resume_text(

            uploaded_file

        )



        # Parse details


        resume_data["job_title"]=""

resume_data["location"]=""

resume_data["experience"] = resume_data.get(
    "experience",
    []
)

resume_data["projects"] = resume_data.get(
    "projects",
    []
)



        # Save session


        st.session_state["resume_text"] = resume_text


        st.session_state["resume_data"] = resume_data



        st.session_state["uploaded"] = True




    st.success(

        "Resume uploaded and analyzed successfully"

    )



    st.divider()






    # -------------------------------
    # Show Extracted Information
    # -------------------------------


    st.subheader(

        "Extracted Resume Details"

    )



    col1,col2 = st.columns(2)



    with col1:


        st.write(

            "### Personal Information"

        )


        st.write(

            "Name:",

            resume_data.get(

                "name",

                ""

            )

        )


        st.write(

            "Email:",

            resume_data.get(

                "email",

                ""

            )

        )


        st.write(

            "Phone:",

            resume_data.get(

                "phone",

                ""

            )

        )





    with col2:


        st.write(

            "### Skills"

        )


        skills = resume_data.get(

            "skills",

            []

        )


        if skills:


            for skill in skills:


                st.write(

                    "✔",

                    skill

                )



        else:


            st.write(

                "No skills detected"

            )





    st.divider()





    # -------------------------------
    # AI Optimization
    # -------------------------------


    st.subheader(

        "AI Resume Optimization"

    )



    if st.button(

        "✨ Optimize Resume"

    ):



        with st.spinner(

            "Optimizing..."

        ):



            optimized = optimize_resume(

                resume_data

            )



            if optimized:


                st.session_state["resume_data"] = optimized



                st.success(

                    "Resume optimized"

                )


            else:


                st.info(

                    "Using original resume data"

                )





    st.divider()





    # -------------------------------
    # Preview
    # -------------------------------


    st.subheader(

        "Resume Preview"

    )


    final_data = st.session_state.get(

        "resume_data",

        resume_data

    )



    with st.expander(

        "View Resume Data"

    ):


        st.json(

            final_data

        )





    st.success(

        "Ready for template generation"

    )




else:


    st.info(

        "Please upload your resume to continue"

    )

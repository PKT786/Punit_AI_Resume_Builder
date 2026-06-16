import streamlit as st
import os


st.set_page_config(
    page_title="Upload Resume",
    page_icon="📄",
    layout="wide"
)


from utils.theme import load_css

load_css()


from utils.resume_parser import (
    extract_resume_text,
    parse_resume
)


from ai.resume_optimizer import optimize_resume





# -------------------------
# Hero Image
# -------------------------

hero = "assets/resume_hero.png"


if os.path.exists(hero):

    st.image(
        hero,
        use_container_width=True
    )



st.title(
    "📄 Upload Resume"
)



st.write(
    "Upload your existing resume and generate a premium ATS resume."
)



st.divider()






uploaded_file = st.file_uploader(

    "Upload DOCX Resume",

    type=["docx"]

)






if uploaded_file:


    with st.spinner("Processing resume..."):


        resume_text = extract_resume_text(
            uploaded_file
        )


        resume_data = parse_resume(
            resume_text
        )


        # Required template fields

        resume_data["job_title"] = ""

        resume_data["location"] = ""


        if "experience" not in resume_data:

            resume_data["experience"] = []


        if "projects" not in resume_data:

            resume_data["projects"] = []



        st.session_state["resume_text"] = resume_text


        st.session_state["resume_data"] = resume_data



    st.success(
        "Resume processed successfully"
    )



    st.divider()



    st.subheader(
        "Extracted Details"
    )


    col1,col2 = st.columns(2)



    with col1:


        st.write(
            "Name"
        )


        st.write(

            resume_data.get(
                "name",
                ""
            )

        )


        st.write(
            "Email"
        )


        st.write(

            resume_data.get(
                "email",
                ""
            )

        )



    with col2:


        st.write(
            "Skills"
        )


        st.write(

            resume_data.get(
                "skills",
                []
            )

        )




    st.divider()



    if st.button(
        "✨ Optimize Resume"
    ):


        optimized = optimize_resume(

            resume_data

        )


        if optimized:


            st.session_state["resume_data"] = optimized


            st.success(
                "Optimization completed"
            )


        else:


            st.info(
                "Using original resume data"
            )



else:


    st.info(
        "Please upload resume file"
   

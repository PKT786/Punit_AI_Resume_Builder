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
# Hero
# -------------------------


hero="assets/resume_hero.png"


if os.path.exists(hero):


    st.image(

        hero,

        use_container_width=True

    )





st.title(

"📄 Upload Existing Resume"

)



st.write(

"Upload your resume and AI will extract details automatically."

)



st.divider()






uploaded_file=st.file_uploader(

    "Upload DOCX Resume",

    type=["docx"]

)





if uploaded_file:



    with st.spinner(

        "Reading resume..."

    ):



        text=extract_resume_text(

            uploaded_file

        )



        resume_data=parse_resume(

            text

        )



        st.session_state["resume_data"]=resume_data



        st.session_state["resume_text"]=text






    st.success(

        "Resume extracted successfully"

    )



    st.divider()



    st.subheader(

        "Extracted Information"

    )




    st.json(

        resume_data

    )





    st.divider()





    if st.button(

        "✨ Optimize Resume"

    ):



        optimized=optimize_resume(

            resume_data

        )



        if optimized:


            st.session_state["resume_data"]=optimized



            st.success(

                "Optimization completed"

            )



    st.divider()



    if st.button(

        "Generate Resume"

    ):



        st.switch_page(

            "pages/4_Download.py"

        )





else:


    st.info(

        "Upload resume to continue"

    )

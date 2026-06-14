import streamlit as st

from utils.resume_parser import extract_resume_text
from ai.resume_optimizer import optimize_resume


st.set_page_config(
    page_title="Upload Resume",
    page_icon="📤",
    layout="wide"
)


st.title("📤 Upload & Build AI Resume")


st.write(
"""
Upload your existing resume and create a premium ATS-friendly resume
using professional templates.
"""
)


uploaded_file = st.file_uploader(

    "Upload Resume",

    type=[
        "pdf",
        "docx"
    ]

)



if uploaded_file:


    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    with st.spinner(
        "Extracting resume information..."
    ):


        resume_text = extract_resume_text(
            uploaded_file
        )



    if resume_text:



        st.subheader(
            "Original Resume Content"
        )


        st.text_area(

            "Extracted Text",

            resume_text,

            height=250

        )


        st.divider()



        template = st.selectbox(

            "Choose Resume Template",

            [

            "Modern Resume",

            "ATS Resume",

            "Developer Resume"

            ]

        )



        st.session_state["template"] = template



        if st.button(

            "🤖 Generate Premium Resume"

        ):



            with st.spinner(

                "AI is improving your resume..."

            ):



                ai_resume = optimize_resume(

                    resume_text,

                    template

                )



            # Store resume data


            st.session_state["resume_data"] = {


                "name":
                "Candidate Name",


                "summary":
                ai_resume,


                "skills":
                "Python | Excel | SQL | AI | Data Analysis",


                "experience":
                ai_resume,


                "projects":
                "AI Resume Builder Project",


                "education":
                "Education Details"

            }




            st.success(

                "Resume generated successfully!"

            )



            st.subheader(

                "Resume Preview"

            )


            st.text_area(

                "",

                ai_resume,

                height=500

            )



            st.info(

            """
            Next:
            Go to Download page
            and export PDF / Word
            """
            )



else:


    st.info(

    """
    Please upload PDF or DOCX resume.

    """

    )

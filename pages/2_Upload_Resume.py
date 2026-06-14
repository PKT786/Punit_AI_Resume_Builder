import streamlit as st

from utils.resume_parser import extract_resume_text

from ai.resume_optimizer import generate_resume_data

from components.preview import show_resume_preview



st.set_page_config(

    page_title="Upload Resume",

    page_icon="📤",

    layout="wide"

)



# -----------------------------
# Page Header
# -----------------------------


st.title(
    "📤 Upload & Generate AI Resume"
)


st.write(

"""
Upload your existing resume.

AI will analyze it and create a professional ATS-friendly resume using your selected template.
"""

)



st.divider()



# -----------------------------
# Upload Resume
# -----------------------------


uploaded_file = st.file_uploader(

    "Upload Resume (PDF/DOCX)",

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

        "Reading resume..."

    ):


        resume_text = extract_resume_text(

            uploaded_file

        )



    if resume_text:



        st.subheader(

            "📄 Extracted Resume"

        )


        st.text_area(

            "Resume Content",

            resume_text,

            height=250

        )



        st.divider()



        # -----------------------------
        # Template Selection
        # -----------------------------


        template = st.selectbox(

            "Choose Resume Template",

            [

            "Modern Resume",

            "ATS Resume",

            "Developer Resume"

            ]

        )



        st.session_state["template"] = template



        st.divider()



        # -----------------------------
        # Generate Resume
        # -----------------------------


        if st.button(

            "🤖 Generate Premium Resume"

        ):



            with st.spinner(

                "AI is analyzing your resume..."

            ):



                resume_data = generate_resume_data(

                    resume_text,

                    template

                )



            # Save structured data


            st.session_state["resume_data"] = resume_data



            st.success(

                "Resume generated successfully!"

            )



            st.divider()



            # Preview


            show_resume_preview(

                resume_data

            )



            st.info(

            """

Next:

1. Check ATS Score

2. Download Word/PDF Resume

            """

            )



    else:


        st.error(

            "Could not extract resume text"

        )



else:


    st.info(

    """

Please upload your resume file.

Supported:

✔ PDF

✔ DOCX

    """

    )

import streamlit as st


from utils.resume_parser import extract_resume_text

from ai.resume_optimizer import optimize_resume



st.set_page_config(

    page_title="Upload Resume",

    page_icon="📤",

    layout="wide"

)



st.title(
"📤 Upload & Optimize Resume"
)



st.write(
"""
Upload your resume and generate a professional ATS-friendly version.
"""
)



uploaded_file = st.file_uploader(

    "Upload PDF / DOCX",

    type=[
        "pdf",
        "docx"
    ]

)



if uploaded_file:


    st.success(
        uploaded_file.name
    )


    with st.spinner(
        "Extracting resume..."
    ):


        resume_text = extract_resume_text(
            uploaded_file
        )



    if resume_text:


        st.subheader(
            "Original Resume"
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

            "ATS Resume",

            "Modern Resume",

            "Developer Resume"

            ]

        )



        if st.button(

            "🤖 Generate Premium Resume"

        ):



            with st.spinner(

                "Creating resume..."

            ):



                final_resume = optimize_resume(

                    resume_text,

                    template

                )



            # Save only resume

            st.session_state["resume"] = final_resume


            st.session_state["template"] = template



            st.success(

                "Resume generated successfully!"

            )



            st.subheader(

                "Resume Preview"

            )



            st.text_area(

                "",

                final_resume,

                height=500

            )



            st.divider()



            col1,col2 = st.columns(2)



            with col1:


                if st.button(
                    "📊 ATS Analysis"
                ):


                    st.switch_page(

                    "pages/3_ATS_Analysis.py"

                    )



            with col2:


                if st.button(

                    "⬇ Download Resume"

                ):


                    st.switch_page(

                    "pages/4_Download.py"

                    )


    else:


        st.error(

        "Unable to read resume"

        )



else:


    st.info(

    """
    Please upload resume file.

    Supported:
    PDF
    DOCX

    """

    )

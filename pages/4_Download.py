import streamlit as st
import os


st.set_page_config(

    page_title="Download Resume",

    page_icon="⬇️",

    layout="wide"

)


from utils.theme import load_css

load_css()



from utils.docx_generator import create_docx



# PDF optional

from utils.pdf_generator import convert_to_pdf





# --------------------------------
# Title
# --------------------------------


st.title(

    "⬇️ Download Your Resume"

)



st.write(

"""
Generate your professional resume using premium templates.

"""

)



st.divider()





# --------------------------------
# Check Session Data
# --------------------------------


if "resume_data" not in st.session_state:



    st.warning(

        "Please upload resume first"

    )


    st.stop()





resume_data = st.session_state["resume_data"]






# --------------------------------
# Template Selection
# --------------------------------


template = st.selectbox(

    "Choose Resume Template",

    [

        "modern_resume.docx",

        "ats_resume.docx",

        "developer_resume.docx"

    ]

)





st.success(

    f"Selected Template: {template}"

)





# --------------------------------
# Generate Resume
# --------------------------------


if st.button(

    "Generate Resume"

):


    with st.spinner(

        "Creating your resume..."

    ):



        docx_file = create_docx(

            template,

            resume_data

        )



        st.session_state["generated_docx"] = docx_file




    st.success(

        "Resume created successfully"

    )







# --------------------------------
# Download DOCX
# --------------------------------


if "generated_docx" in st.session_state:


    docx_path = st.session_state["generated_docx"]



    with open(

        docx_path,

        "rb"

    ) as file:


        st.download_button(

            label="📄 Download DOCX Resume",

            data=file,

            file_name="Professional_Resume.docx",

            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        )






# --------------------------------
# PDF Download
# --------------------------------


st.divider()



st.subheader(

    "PDF Version"

)





if "generated_docx" in st.session_state:


    if st.button(

        "Create PDF"

    ):



        with st.spinner(

            "Creating PDF..."

        ):



            pdf_file = convert_to_pdf(

                st.session_state["generated_docx"]

            )



            st.session_state["generated_pdf"] = pdf_file




if "generated_pdf" in st.session_state:


    pdf_path = st.session_state["generated_pdf"]



    with open(

        pdf_path,

        "rb"

    ) as file:


        st.download_button(

            label="📕 Download PDF Resume",

            data=file,

            file_name="Professional_Resume.pdf",

            mime="application/pdf"

        )





# --------------------------------
# Preview
# --------------------------------


st.divider()


st.subheader(

    "Resume Data Preview"

)



st.json(

    resume_data

)

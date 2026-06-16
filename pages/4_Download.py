import streamlit as st
import os



# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(

    page_title="Download Resume",

    page_icon="⬇️",

    layout="wide"

)



# -----------------------------
# CSS
# -----------------------------

from utils.theme import load_css

load_css()



# -----------------------------
# Imports
# -----------------------------

from utils.docx_generator import create_docx

from utils.pdf_generator import convert_to_pdf



# -----------------------------
# Hero
# -----------------------------


def hero():


    image="assets/download.png"



    col1,col2 = st.columns(2)



    with col1:


        st.title(

            "⬇️ Download Resume"

        )


        st.write(

        """

        Generate your professional resume.

        Choose template and download DOCX/PDF.

        """

        )



    with col2:


        if os.path.exists(image):

            st.image(

                image,

                use_container_width=True

            )



hero()



st.divider()



# -----------------------------
# Check Resume Data
# -----------------------------


if "resume" not in st.session_state:


    st.warning(

    """

    No resume data found.

    Please create or upload resume first.

    """

    )


    st.page_link(

        "pages/1_Create_Resume.py",

        label="📝 Create Resume"

    )


    st.page_link(

        "pages/2_Upload_Resume.py",

        label="📂 Upload Resume"

    )


    st.stop()



resume_data = st.session_state["resume"]




# -----------------------------
# Show Resume Details
# -----------------------------


st.subheader(

"Resume Preview"

)


col1,col2 = st.columns(2)



with col1:


    st.write(

        "Name",

        resume_data.get(

            "name",

            ""

        )

    )


    st.write(

        "Email",

        resume_data.get(

            "email",

            ""

        )

    )



with col2:


    st.write(

        "Role",

        resume_data.get(

            "job_title",

            ""

        )

    )


    st.write(

        "Skills",

        ", ".join(

            resume_data.get(

                "skills",

                []

            )

        )

    )



st.divider()



# -----------------------------
# Template Selection
# -----------------------------


st.subheader(

"Select Resume Template"

)



template = st.selectbox(

"Choose Template",

[

"modern_resume.docx",

"ats_resume.docx",

"developer_resume.docx"

]

)



st.divider()



# -----------------------------
# Generate DOCX
# -----------------------------


if st.button(

"Generate DOCX Resume"

):


    with st.spinner(

        "Creating resume..."

    ):



        docx_file = create_docx(

            template,

            resume_data

        )



        st.session_state["docx_file"] = docx_file



    st.success(

    "DOCX Resume Generated Successfully"

    )




# Download DOCX


if "docx_file" in st.session_state:


    with open(

        st.session_state["docx_file"],

        "rb"

    ) as file:


        st.download_button(

            label="⬇ Download DOCX",

            data=file,

            file_name="Professional_Resume.docx",

            mime=

            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        )



st.divider()



# -----------------------------
# Generate PDF
# -----------------------------


if st.button(

"Generate PDF Resume"

):


    if "docx_file" not in st.session_state:


        st.error(

        "First generate DOCX resume"

        )


    else:



        with st.spinner(

            "Creating PDF..."

        ):



            pdf_file = convert_to_pdf(

                st.session_state["docx_file"]

            )



            st.session_state["pdf_file"] = pdf_file



        st.success(

        "PDF Generated Successfully"

        )





# Download PDF


if "pdf_file" in st.session_state:


    with open(

        st.session_state["pdf_file"],

        "rb"

    ) as file:


        st.download_button(

            label="⬇ Download PDF",

            data=file,

            file_name="Professional_Resume.pdf",

            mime="application/pdf"

        )

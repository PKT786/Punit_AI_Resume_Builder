import streamlit as st

from utils.docx_generator import create_docx

from utils.pdf_generator import convert_docx_to_pdf



st.set_page_config(

    page_title="Download Resume",

    page_icon="📄",

    layout="wide"

)



st.title(
"📄 Download Resume"
)



if "resume_data" not in st.session_state:


    st.warning(

    "Please generate resume first"

    )


    st.stop()



resume_data = st.session_state["resume_data"]


template = st.session_state["template"]



st.subheader(

"Selected Template"

)


st.success(

template

)



st.divider()



st.subheader(

"Resume Preview"

)


st.text_area(

"",

resume_data["summary"],

height=400

)



st.divider()



if st.button(

"Generate Files"

):


    with st.spinner(

        "Creating professional files..."

    ):



        # Create DOCX from template


        docx_file = create_docx(

            resume_data,

            template

        )



        # Convert same DOCX to PDF


        pdf_file = convert_docx_to_pdf(

            docx_file

        )



        st.session_state["docx_file"] = docx_file


        st.session_state["pdf_file"] = pdf_file



    st.success(

        "Files ready!"

    )





if "docx_file" in st.session_state:


    col1,col2 = st.columns(2)



    with col1:


        with open(

            st.session_state["docx_file"],

            "rb"

        ) as file:


            st.download_button(

                "⬇ Download Word",

                file,

                file_name="AI_Resume.docx"

            )




    with col2:


        with open(

            st.session_state["pdf_file"],

            "rb"

        ) as file:


            st.download_button(

                "⬇ Download PDF",

                file,

                file_name="AI_Resume.pdf"

            )

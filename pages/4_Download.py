import streamlit as st


from utils.docx_generator import create_docx

from utils.pdf_generator import create_pdf



st.set_page_config(
    page_title="Download Resume",
    layout="wide"
)



st.title(
"📄 Download Your Resume"
)



if "resume" not in st.session_state:


    st.warning(
    "Generate resume first"
    )


else:


    resume = st.session_state["resume"]



    st.subheader(
    "Resume Preview"
    )


    st.text_area(
        "",
        resume,
        height=400
    )



    docx_file = create_docx(
        resume
    )


    pdf_file = create_pdf(
        resume
    )



    col1,col2 = st.columns(2)



    with col1:


        with open(docx_file,"rb") as f:


            st.download_button(

            "⬇ Download Word",

            f,

            file_name=
            "AI_Resume.docx"

            )



    with col2:


        with open(pdf_file,"rb") as f:


            st.download_button(

            "⬇ Download PDF",

            f,

            file_name=
            "AI_Resume.pdf"

            )

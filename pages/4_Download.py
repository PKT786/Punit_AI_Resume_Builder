import streamlit as st


from utils.docx_generator import create_docx

from utils.pdf_generator import create_pdf



st.set_page_config(

    page_title="Download Resume",

    page_icon="📄",

    layout="wide"

)



st.title(
"📄 Download Your Resume"
)



if "resume" not in st.session_state:


    st.warning(

    "Please generate resume first"

    )


    st.stop()



resume = st.session_state["resume"]



st.subheader(

"Resume Preview"

)



st.text_area(

"",

resume,

height=500

)



st.divider()



with st.spinner(

"Preparing files..."

):


    docx_file = create_docx(

        resume

    )


    pdf_file = create_pdf(

        resume

    )




col1,col2 = st.columns(2)



with col1:


    with open(
        docx_file,
        "rb"
    ) as file:


        st.download_button(

            label="⬇ Download Word",

            data=file,

            file_name="AI_Resume.docx",

            mime=
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        )



with col2:


    with open(

        pdf_file,

        "rb"

    ) as file:


        st.download_button(

            label="⬇ Download PDF",

            data=file,

            file_name="AI_Resume.pdf",

            mime="application/pdf"

        )

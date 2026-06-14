import streamlit as st


from utils.docx_generator import create_docx

from utils.pdf_generator import convert_docx_to_pdf



st.set_page_config(

    page_title="Download Resume",

    page_icon="📄",

    layout="wide"

)



st.title(

    "📄 Download Your Resume"

)



# ---------------------------------
# Check Resume Exists
# ---------------------------------


if "resume_data" not in st.session_state:


    st.warning(

        "Please generate resume first."

    )


    st.stop()



resume_data = st.session_state["resume_data"]



template = st.session_state.get(

    "template",

    "ATS Resume"

)



st.subheader(

    "Selected Template"

)



st.success(

    template

)



st.divider()



# ---------------------------------
# Preview
# ---------------------------------


st.subheader(

    "Resume Preview"

)



resume_content = resume_data["summary"]



st.text_area(

    "Generated Resume",

    resume_content,

    height=450

)



st.divider()



# ---------------------------------
# Generate Files
# ---------------------------------


if st.button(

    "⚙️ Create Download Files"

):


    with st.spinner(

        "Preparing DOCX and PDF..."

    ):


        # Create DOCX using template


        docx_file = create_docx(

            resume_data,

            template

        )



        # Create PDF


        pdf_file = convert_docx_to_pdf(

            docx_file,

            resume_content

        )



        st.session_state["docx_file"] = docx_file

        st.session_state["pdf_file"] = pdf_file



    st.success(

        "Files created successfully!"

    )



st.divider()



# ---------------------------------
# Download Buttons
# ---------------------------------


if "docx_file" in st.session_state:



    col1,col2 = st.columns(2)



    with col1:


        with open(

            st.session_state["docx_file"],

            "rb"

        ) as file:


            st.download_button(

                label="⬇ Download Word Resume",

                data=file,

                file_name="AI_Resume.docx",

                mime=
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            )



    with col2:


        with open(

            st.session_state["pdf_file"],

            "rb"

        ) as file:


            st.download_button(

                label="⬇ Download PDF Resume",

                data=file,

                file_name="AI_Resume.pdf",

                mime="application/pdf"

            )

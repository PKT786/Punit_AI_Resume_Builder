import streamlit as st

from resume_parser import extract_resume_text
from ai_optimizer import optimize_resume
from resume_generator import create_word_resume, create_pdf_resume


st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Builder & ATS Optimizer")

st.write(
    """
Create your professional ATS-friendly resume using AI.

Upload your existing resume or enter your details manually.
Generate PDF and Word resume instantly.
"""
)


option = st.radio(
    "Choose Resume Method",
    [
        "Create New Resume",
        "Upload Existing Resume"
    ]
)


resume_content = ""


# -----------------------------
# OPTION 1
# -----------------------------

if option == "Create New Resume":

    st.subheader("Personal Information")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone")


    st.subheader("Professional Summary")

    summary = st.text_area(
        "About Yourself"
    )


    st.subheader("Skills")

    skills = st.text_area(
        "Example: Python, Excel, SQL, AI"
    )


    st.subheader("Experience")

    experience = st.text_area(
        "Work Experience"
    )


    st.subheader("Education")

    education = st.text_area(
        "Education Details"
    )


    resume_content = f"""

{name}

Email:
{email}

Phone:
{phone}


Professional Summary:

{summary}


Skills:

{skills}


Experience:

{experience}


Education:

{education}

"""


# -----------------------------
# OPTION 2
# -----------------------------


else:

    st.subheader(
        "Upload Resume"
    )


    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=[
            "pdf",
            "docx"
        ]
    )


    if uploaded_file:

        resume_content = extract_resume_text(
            uploaded_file
        )


        st.success(
            "Resume extracted successfully"
        )


        st.text_area(
            "Extracted Resume",
            resume_content,
            height=300
        )



# -----------------------------
# AI OPTIMIZATION
# -----------------------------


if st.button(
    "🤖 Optimize Resume With AI"
):

    if resume_content:

        optimized_resume = optimize_resume(
            resume_content
        )


        st.session_state[
            "resume"
        ] = optimized_resume


        st.success(
            "Resume optimized"
        )


        st.text_area(
            "AI Improved Resume",
            optimized_resume,
            height=400
        )


    else:

        st.warning(
            "Please add resume details"
        )



# -----------------------------
# DOWNLOAD
# -----------------------------


if "resume" in st.session_state:


    st.divider()


    st.subheader(
        "Download Resume"
    )


    word_file = create_word_resume(
        st.session_state["resume"]
    )


    pdf_file = create_pdf_resume(
        st.session_state["resume"]
    )


    with open(word_file,"rb") as f:

        st.download_button(
            "⬇ Download Word",
            f,
            file_name="AI_Resume.docx"
        )



    with open(pdf_file,"rb") as f:

        st.download_button(
            "⬇ Download PDF",
            f,
            file_name="AI_Resume.pdf"
        )
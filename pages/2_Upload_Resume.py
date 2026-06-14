import streamlit as st

from utils.resume_parser import extract_resume_text
from ai.resume_optimizer import optimize_resume


st.set_page_config(
    page_title="Upload Resume",
    layout="wide"
)


st.title("📤 Upload Existing Resume")


st.write(
"""
Upload your existing resume and AI will:
- Analyze content
- Improve wording
- Optimize ATS keywords
"""
)


uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf","docx"]
)



if uploaded_file:


    resume_text = extract_resume_text(
        uploaded_file
    )


    st.subheader(
        "Extracted Resume"
    )


    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )


    if st.button(
        "🤖 Optimize With AI"
    ):


        optimized = optimize_resume(
            resume_text
        )


        st.session_state["resume"] = optimized


        st.success(
            "Resume optimized successfully"
        )


        st.text_area(
            "AI Improved Resume",
            optimized,
            height=400
        )
import streamlit as st


# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(

    page_title="ATS Resume Checker",

    page_icon="📊",

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

from utils.resume_parser import (

    extract_resume_text,

    parse_resume

)



from utils.ats_checker import calculate_ats_score




# -----------------------------
# Title
# -----------------------------


st.title(

    "📊 ATS Resume Analyzer"

)



st.write(

"""
Upload your resume and check:

✅ ATS Score

✅ Missing Keywords

✅ Resume Quality

✅ Improvement Suggestions

"""

)



st.divider()



# -----------------------------
# Upload
# -----------------------------


uploaded_file = st.file_uploader(

    "Upload Resume",

    type=["docx"]

)



if uploaded_file:



    # Extract Text


    text = extract_resume_text(

        uploaded_file

    )



    # Convert Data


    resume_data = parse_resume(

        text

    )



    # Save Session


    st.session_state["resume"] = resume_data



    st.success(

        "Resume analyzed successfully"

    )



    st.divider()



    # ATS


    result = calculate_ats_score(

        text

    )



    st.subheader(

        "ATS Score"

    )



    col1,col2 = st.columns(2)



    with col1:


        st.metric(

            "Score",

            f"{result['score']}%"

        )



    with col2:


        st.progress(

            result["score"] / 100

        )



    st.divider()



    st.subheader(

        "Suggestions"

    )



    for item in result["suggestions"]:


        st.write(

            "✔ " + item

        )



    st.divider()



    st.subheader(

        "Extracted Resume Data"

    )


    st.json(

        resume_data

    )

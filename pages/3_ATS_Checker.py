import streamlit as st

from utils.theme import load_css


load_css()


st.title(
"AI Resume Builder"
)
import streamlit as st


from utils.resume_parser import (
    extract_resume_text,
    parse_resume
)

from utils.ats_checker import calculate_ats_score



st.set_page_config(

page_title="ATS Resume Checker",

page_icon="📊"

)



st.title(
"📊 ATS Resume Score Checker"
)



st.write(

"""
Check how compatible your resume is with Applicant Tracking Systems.

Upload resume and get:

✔ ATS Score

✔ Missing keywords

✔ Improvement suggestions

"""

)



resume = st.file_uploader(

"Upload Resume",

type=["docx"]

)



job = st.text_area(

"Paste Job Description (optional)"

)



if resume:


    text = extract_resume(

        resume

    )



    result = calculate_ats_score(

        text,

        job

    )



    st.divider()



    score=result["score"]



    st.metric(

    "ATS Score",

    f"{score}%"

    )



    if score>=80:


        st.success(

        "Excellent ATS compatibility"

        )


    elif score>=60:


        st.warning(

        "Needs improvement"

        )


    else:


        st.error(

        "Resume needs optimization"

        )



    st.subheader(

    "✅ Skills Found"

    )


    st.write(

    result["skills_found"]

    )



    st.subheader(

    "💡 Suggestions"

    )


    for item in result["suggestions"]:


        st.write(

        "• "+item

        )

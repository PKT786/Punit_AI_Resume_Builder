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

from ai.resume_optimizer import optimize_resume
from utils.ui_components import hero_section

hero_section(

"upload_resume.png",

"Upload Existing Resume",

"Analyze, improve and convert your resume into professional format"

)



st.set_page_config(

    page_title="Upload Resume",

    page_icon="📂",

    layout="wide"

)



st.title("📂 Upload Existing Resume")

st.write(

"""
Upload your existing resume.

System will:

✔ Extract information

✔ Check ATS score

✔ Optimize using AI (optional)

✔ Prepare it for templates

"""

)



uploaded_file = st.file_uploader(

    "Upload DOCX Resume",

    type=["docx"]

)



if uploaded_file:



    st.success(

        "Resume uploaded successfully"

    )


    # -------------------------
    # Extract Resume Text
    # -------------------------


    resume_text = extract_resume_text(
    uploaded_file
)
    resume_data = parse_resume(
    resume_text
)


st.session_state["resume"] = resume_data



    st.subheader(

        "📄 Extracted Resume Content"

    )


    with st.expander(

        "View Extracted Text"

    ):


        st.write(

            resume_text

        )



    # -------------------------
    # ATS Score
    # -------------------------


    ats_result = calculate_ats_score(

        resume_text

    )


    st.divider()



    st.subheader(

        "📊 ATS Score"

    )


    st.metric(

        "Resume Score",

        f"{ats_result['score']}%"

    )



    if ats_result["score"] >= 80:


        st.success(

            "Excellent ATS compatibility"

        )


    elif ats_result["score"] >= 60:


        st.warning(

            "Resume can be improved"

        )


    else:


        st.error(

            "Resume needs optimization"

        )



    st.write(

        "Suggestions"

    )


    for s in ats_result["suggestions"]:


        st.write(

            "• " + s

        )



    # -------------------------
    # Prepare Resume Data
    # -------------------------


    resume_data = {


        "name":"",

        "job_title":"",

        "email":"",

        "phone":"",

        "summary":resume_text[:500],


        "skills":"",

        "experience":resume_text,


        "education":""



    }



    # -------------------------
    # AI Optimization
    # -------------------------


    if st.button(

        "🤖 Optimize With AI"

    ):



        with st.spinner(

            "AI improving resume..."

        ):


            optimized = optimize_resume(

                resume_text

            )



            resume_data["summary"] = optimized



        st.success(

            "AI optimization completed"

        )



    else:


        st.info(

            "Using extracted resume data"

        )



    # -------------------------
    # SESSION STORAGE
    # -------------------------


    st.session_state["resume_data"] = resume_data


    st.session_state["ats_result"] = ats_result



    st.success(

        "Resume data saved. Go to Download page."

    )
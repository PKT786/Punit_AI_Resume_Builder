import streamlit as st


from utils.theme import load_css


load_css()



from utils.resume_parser import (
    extract_resume_text,
    parse_resume
)


from utils.ats_checker import calculate_ats_score


from ai.resume_optimizer import optimize_resume



st.set_page_config(

    page_title="Upload Resume",

    page_icon="📂",

    layout="wide"

)



st.title(
    "📂 Upload Existing Resume"
)



st.write(
"""
Upload your existing resume.

The system will:

✔ Extract resume information

✔ Check ATS score

✔ Prepare resume for templates

✔ Generate DOCX/PDF

"""
)



uploaded_file = st.file_uploader(

    "Upload Resume",

    type=["docx"]

)



if uploaded_file:


    st.success(
        "Resume uploaded successfully"
    )


    # Extract text

    resume_text = extract_resume_text(

        uploaded_file

    )



    with st.expander(
        "View Extracted Resume"
    ):

        st.write(

            resume_text

        )



    # Parse data

    resume_data = parse_resume(

        resume_text

    )



    # Save session

    st.session_state["resume"] = resume_data



    # ATS Analysis

    ats_result = calculate_ats_score(

        resume_text

    )


    st.session_state["ats_result"] = ats_result



    st.divider()



    st.subheader(
        "📊 ATS Score"
    )



    st.metric(

        "Resume Score",

        f"{ats_result['score']}%"

    )



    for item in ats_result["suggestions"]:


        st.write(

            "• " + item

        )



    st.divider()



    if st.button(

        "🤖 Optimize Resume With AI"

    ):


        with st.spinner(

            "Improving resume..."

        ):


            optimized = optimize_resume(

    resume_data

)



if isinstance(optimized, dict):


    st.session_state["resume"] = optimized


else:


    resume_data["summary"] = optimized


    st.session_state["resume"] = resume_data



        st.success(

            "AI optimization completed"

        )



    st.success(

        "Resume data saved successfully. Go to Download page."

    )
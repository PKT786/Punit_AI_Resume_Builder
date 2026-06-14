import streamlit as st

from ai.ats_checker import check_ats



st.set_page_config(
    page_title="ATS Analysis",
    layout="wide"
)


st.title(
"📊 ATS Resume Analysis"
)



if "resume" not in st.session_state:


    st.warning(
    "Please upload and optimize resume first"
    )


else:


    resume = st.session_state["resume"]



    result = check_ats(
        resume
    )


    score = result["score"]


    st.metric(
        "ATS Score",
        f"{score}/100"
    )


    col1,col2,col3 = st.columns(3)



    with col1:

        st.success(
        f"""
        Keyword Match

        {result['keywords']}%
        """
        )



    with col2:

        st.info(
        f"""
        Formatting

        {result['format']}%
        """
        )



    with col3:

        st.warning(
        f"""
        Skills

        {result['skills']}%
        """
        )



    st.subheader(
    "AI Suggestions"
    )


    for item in result["suggestions"]:

        st.write(
        "✓ " + item
        )

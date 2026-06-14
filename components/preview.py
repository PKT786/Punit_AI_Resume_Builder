import streamlit as st


def show_resume_preview(resume):


    st.subheader(
        "👁 Live Resume Preview"
    )


    with st.container():


        st.markdown(
        f"""
        <div style="
        border:1px solid #ddd;
        padding:30px;
        border-radius:15px;
        background:white;
        ">


        <h2>
        AI Generated Resume
        </h2>


        <hr>


        {resume.replace(chr(10),'<br>')}


        </div>

        """,
        unsafe_allow_html=True

        )
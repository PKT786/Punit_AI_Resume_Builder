import streamlit as st

from utils.resume_parser import extract_resume_text

from ai.resume_optimizer import optimize_resume



st.set_page_config(

    page_title="Upload Resume",

    page_icon="📤",

    layout="wide"

)



# -----------------------------
# Custom Styling
# -----------------------------


st.markdown(
"""
<style>


.main-title{

font-size:45px;

font-weight:800;

}



.info-box{

padding:20px;

border-radius:15px;

background:#f3f4f6;

}


.stButton button{


width:100%;

height:50px;

border-radius:10px;

font-size:18px;

font-weight:600;


}


</style>

""",

unsafe_allow_html=True

)



# -----------------------------
# Header
# -----------------------------


st.markdown(

"""

<div class="main-title">

📤 Upload & Optimize Resume

</div>


<p>

Upload your existing resume and let AI transform it into an ATS-friendly professional resume.

</p>


""",

unsafe_allow_html=True

)



st.divider()



# -----------------------------
# Upload Section
# -----------------------------


uploaded_file = st.file_uploader(

    "Upload your Resume (PDF / DOCX)",

    type=[
        "pdf",
        "docx"
    ]

)



if uploaded_file:



    st.success(

        f"Uploaded: {uploaded_file.name}"

    )



    # Extract text


    with st.spinner(
        "Reading resume..."
    ):


        resume_text = extract_resume_text(

            uploaded_file

        )



    if resume_text:


        st.session_state["original_resume"] = resume_text



        st.subheader(

            "📄 Resume Content"

        )


        st.text_area(

            "Extracted Content",

            resume_text,

            height=250

        )



        st.divider()



        # -----------------------------
        # Template Selection
        # -----------------------------



        st.subheader(

            "🎨 Choose Resume Style"

        )


        template = st.selectbox(

            "Select Template",

            [

                "ATS Resume",

                "Modern Resume",

                "Developer Resume"

            ]

        )



        st.session_state["template"] = template



        st.divider()



        # -----------------------------
        # Optimize Button
        # -----------------------------



        if st.button(

            "🤖 Generate Premium Resume"

        ):



            with st.spinner(

                "AI is improving your resume..."

            ):



                optimized_resume = optimize_resume(

                    resume_text,

                    template

                )



            st.session_state["resume"] = optimized_resume



            st.success(

                "Resume generated successfully!"

            )



            st.divider()



            st.subheader(

                "✨ AI Generated Resume Preview"

            )



            st.text_area(

                "Final Resume",

                optimized_resume,

                height=500

            )



            st.info(

            """

Next Steps:

1. Check ATS Score

2. Download PDF/DOCX

            """

            )



    else:


        st.error(

            "Unable to extract resume content."

        )



else:


    st.info(

    """

Please upload your resume file.

Supported:

✔ PDF

✔ DOCX

    """

    )



# -----------------------------
# Navigation
# -----------------------------


if "resume" in st.session_state:


    st.divider()


    col1,col2 = st.columns(2)



    with col1:


        if st.button(

            "📊 Check ATS Score"

        ):


            st.switch_page(

            "pages/3_ATS_Analysis.py"

            )



    with col2:


        if st.button(

            "⬇ Download Resume"

        ):


            st.switch_page(

            "pages/4_Download.py"

            )

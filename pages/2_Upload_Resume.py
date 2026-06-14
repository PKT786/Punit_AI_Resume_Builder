import streamlit as st
import os


from utils.resume_parser import extract_resume_text

from ai.resume_optimizer import generate_resume_data

from components.preview import show_resume_preview



# -----------------------------
# Page Configuration
# -----------------------------


st.set_page_config(

    page_title="AI Resume Builder",

    page_icon="📄",

    layout="wide"

)



# -----------------------------
# Custom CSS
# -----------------------------


st.markdown(

"""

<style>


.hero-title{

font-size:45px;

font-weight:800;

color:#111827;

}



.hero-text{

font-size:20px;

color:#4b5563;

}



.stButton button{


width:100%;

height:50px;

border-radius:12px;

font-size:17px;

font-weight:600;


}


</style>


""",

unsafe_allow_html=True

)



# -----------------------------
# Hero Section
# -----------------------------


hero_image = "assets/resume_hero.png"



hero_col1, hero_col2 = st.columns(
    [1,1]
)



with hero_col1:


    st.markdown(

    """

    <div class="hero-title">

    📄 AI Resume Builder

    </div>


    """,

    unsafe_allow_html=True

    )



    st.markdown(

    """

    <div class="hero-text">

    Create ATS-friendly professional resumes using AI.


    <br><br>


    ✔ AI Resume Optimization

    <br>

    ✔ ATS Keyword Improvement

    <br>

    ✔ PDF & Word Export

    <br>

    ✔ Professional Templates


    </div>


    """,

    unsafe_allow_html=True

    )





with hero_col2:


    if os.path.exists(hero_image):


        st.image(

            hero_image,

            use_container_width=True

        )


    else:


        st.warning(

            "Hero image not found. Add assets/resume_hero.png"

        )



st.divider()



# -----------------------------
# Upload Section
# -----------------------------


st.header(
    "📤 Upload Your Resume"
)



uploaded_file = st.file_uploader(

    "Upload PDF or DOCX file",

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



        st.subheader(

            "📄 Extracted Resume Content"

        )



        st.text_area(

            "Resume Text",

            resume_text,

            height=250

        )



        st.divider()



        # -----------------------------
        # Template Selection
        # -----------------------------



        st.subheader(

            "🎨 Select Resume Template"

        )



        template = st.selectbox(

            "Choose Style",

            [

                "Modern Resume",

                "ATS Resume",

                "Developer Resume"

            ]

        )



        st.session_state["template"] = template



        st.divider()



        # -----------------------------
        # Generate Button
        # -----------------------------



        if st.button(

            "🤖 Generate Premium Resume"

        ):



            with st.spinner(

                "AI is analyzing your resume..."

            ):



                resume_data = generate_resume_data(

                    resume_text,

                    template

                )



            # Save data


            st.session_state["resume_data"] = resume_data



            st.success(

                "Resume generated successfully!"

            )



            st.divider()



            # Preview


            show_resume_preview(

                resume_data

            )



            st.info(

            """

            Next:

            Go to Download page

            Generate Word/PDF resume

            """

            )



    else:


        st.error(

            "Unable to extract resume information"

        )



else:


    st.info(

    """

    Upload your resume to start.

    Supported:

    ✔ PDF

    ✔ DOCX


    """

    )

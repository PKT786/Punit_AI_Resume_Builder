import streamlit as st

from utils.theme import load_css


load_css()


st.title(
"AI Resume Builder"
)
import streamlit as st


from utils.docx_generator import create_docx
from utils.ui_components import hero_section

hero_section(

"download.png",

"Download Your Resume",

"Choose template and generate DOCX/PDF resume"

)

st.set_page_config(

    page_title="Download Resume",

    page_icon="⬇️"

)



st.title(

"⬇️ Download Resume"

)



if "resume_data" not in st.session_state:


    st.warning(

    "Please upload resume first"

    )


    st.stop()



resume_data = st.session_state["resume"]



template = st.selectbox(

"Choose Template",

[

"modern_resume.docx",

"ats_resume.docx",

"developer_resume.docx"

]

)



if st.button(

"Generate Resume"

):


    file = create_docx(

        template,

        resume_data

    )



    with open(file,"rb") as f:


        st.download_button(


            label="Download DOCX",

            data=f,

            file_name=file,

            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"


        )
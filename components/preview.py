import streamlit as st



def show_resume_preview(resume_data):


    st.subheader(

        "👁 Resume Preview"

    )



    preview = f"""

# {resume_data.get('name','Candidate Name')}


## Professional Summary

{resume_data.get('summary','')}


## Skills

{resume_data.get('skills','')}


## Experience

{resume_data.get('experience','')}


## Projects

{resume_data.get('projects','')}


## Education

{resume_data.get('education','')}

"""



    st.markdown(

        preview

    )



    st.divider()



    st.download_button(

        label="📋 Copy Resume Text",

        data=preview,

        file_name="resume_preview.txt"

    )

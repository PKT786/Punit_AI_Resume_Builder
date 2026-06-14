import streamlit as st


st.title(
"Create Resume"
)


name = st.text_input(
"Full Name"
)


role = st.text_input(
"Job Role"
)


skills = st.text_area(
"Skills"
)



if st.button(
"Generate Resume"
):

    st.success(
    "Resume Created"
    )

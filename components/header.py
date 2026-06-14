import streamlit as st


def hero():

    st.markdown(
    """

<div style="
padding:40px;
border-radius:20px;
background:
linear-gradient(
135deg,
#eef2ff,
#ecfeff
);
">


<h1 style="
font-size:55px;
color:#111827;
">

📄 AI Resume Builder

</h1>


<h2>

Build ATS-Friendly Resume with AI

</h2>


<p style="
font-size:20px;
color:#4b5563;
">

Generate professional resumes,
improve keywords,
match jobs,
and increase interview chances.

</p>


</div>


""",
unsafe_allow_html=True
)

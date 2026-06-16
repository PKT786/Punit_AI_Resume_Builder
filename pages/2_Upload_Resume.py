import streamlit as st
import os



# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(

    page_title="Upload Resume",

    page_icon="📂",

    layout="wide"

)



# -----------------------------
# Load CSS
# -----------------------------

from utils.theme import load_css

load_css()



# -----------------------------
# Imports
# -----------------------------

from utils.resume_parser import (

    extract_resume_text,

    parse_resume

)



from utils.ats_checker import calculate_ats_score



from ai.resume_optimizer import optimize_resume



# -----------------------------
# Hero Section
# -----------------------------

def show_hero():


    image_path = os.path.join(

        "assets",

        "upload_resume.png"

    )



    col1, col2 = st.columns(

        [1,1]

    )



    with col1:


        st.title(

            "📂 Upload Existing Resume"

        )


        st.write(

        """

        Upload your existing resume and our system will:

        ✅ Extract information

        ✅ Check ATS compatibility

        ✅ Improve resume content

        ✅ Generate professional DOCX/PDF resume

        """

        )



    with col2:


        if os.path.exists(image_path):


            st.image(

                image_path,

                use_container_width=True

            )



show_hero()



st.divider()



# -----------------------------
# Upload Resume
# -----------------------------


uploaded_file = st.file_uploader(

    "Upload Resume (DOCX)",

    type=[

        "docx"

    ]

)



if uploaded_file:


    st.success(

        "Resume uploaded successfully ✅"

    )



    # -------------------------
    # Extract Text
    # -------------------------


    resume_text = extract_resume_text(

        uploaded_file

    )



    with st.expander(

        "View Extracted Resume Text"

    ):


        st.write(

            resume_text

        )



    # -------------------------
    # Convert to JSON
    # -------------------------


    resume_data = parse_resume(

        resume_text

    )



    # Store session


    st.session_state["resume"] = resume_data



    # -------------------------
    # Show Extracted Details
    # -------------------------


    st.subheader(

        "📌 Extracted Information"

    )


    col1,col2 = st.columns(2)



    with col1:


        st.write(

            "Name:",

            resume_data.get(

                "name",

                ""

            )

        )


        st.write(

            "Email:",

            resume_data.get(

                "email",

                ""

            )

        )



    with col2:


        st.write(

            "Phone:",

            resume_data.get(

                "phone",

                ""

            )

        )


        st.write(

            "Skills:",

            ", ".join(

                resume_data.get(

                    "skills",

                    []

                )

            )

        )



    st.divider()



    # -------------------------
    # ATS SCORE
    # -------------------------


    st.subheader(

        "📊 ATS Analysis"

    )



    ats_result = calculate_ats_score(

        resume_text

    )



    st.session_state["ats_result"] = ats_result



    col1,col2 = st.columns(2)



    with col1:


        st.metric(

            "ATS Score",

            f"{ats_result['score']}%"

        )



    with col2:


        st.progress(

            ats_result["score"]/100

        )



    for suggestion in ats_result["suggestions"]:


        st.write(

            "• " + suggestion

        )



    st.divider()



    # -------------------------
    # AI Optimization
    # -------------------------


    st.subheader(

        "🤖 AI Resume Optimization"

    )



    if st.button(

        "Improve Resume Using AI"

    ):



        with st.spinner(

            "Optimizing resume..."

        ):



            optimized = optimize_resume(

                resume_data

            )



            # If AI returns dictionary

            if isinstance(

                optimized,

                dict

            ):


                st.session_state["resume"] = optimized



            else:


                # AI text response

                resume_data["summary"] = optimized


                st.session_state["resume"] = resume_data



        st.success(

            "Resume optimized successfully ✅"

        )



    else:


        st.info(

        "AI optimization is optional. Resume generation will work without AI."

        )



    st.divider()



    st.success(

    """

    Resume data saved successfully.

    Now go to:

    Download Resume → Generate DOCX/PDF

    """

    )
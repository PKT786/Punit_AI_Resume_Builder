from ai.openai_client import get_openai_client
import streamlit as st
import json


def generate_resume_data(resume_text, template):

    try:

        client = get_openai_client()


        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {

                "role":"system",

                "content":
                f"""

You are an ATS resume expert.

Analyze the resume and return ONLY JSON.

Template:
{template}


Return format:

{{
"name":"",
"summary":"",
"skills":"",
"experience":"",
"projects":"",
"education":""
}}

Do not add explanation.

"""

                },


                {

                "role":"user",

                "content":resume_text

                }

            ]

        )


        result = response.choices[0].message.content


        return json.loads(result)



    except Exception as e:


        st.warning(
            "AI unavailable. Creating basic resume."
        )


        return {


        "name":"Candidate Name",


        "summary":resume_text,


        "skills":
        "Technical Skills",


        "experience":
        resume_text,


        "projects":
        "Project Details",


        "education":
        "Education Details"


        }

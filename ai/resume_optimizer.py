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

                    "content":"""

You are an expert ATS resume parser.

Read the resume and extract information.

Return ONLY valid JSON.

Format:

{
"name":"",
"summary":"",
"skills":"",
"experience":"",
"projects":"",
"education":""
}

Do not add markdown.
Do not add explanation.

"""
                },


                {

                "role":"user",

                "content":resume_text

                }

            ],

            temperature=0

        )



        result=response.choices[0].message.content



        # remove markdown if AI adds it

        result=result.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()



        data=json.loads(result)



        return data



    except Exception as e:


        st.warning(
            "AI extraction failed, using resume text fallback"
        )


        return {


        "name":"Candidate Name",

        "summary":resume_text,

        "skills":"",

        "experience":"",

        "projects":"",

        "education":""


        }

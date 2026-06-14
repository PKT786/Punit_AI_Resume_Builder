from openai import OpenAI
import streamlit as st


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


def optimize_resume(resume):

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role":"system",
                "content":
                """
                You are an expert ATS resume writer.
                Improve resumes professionally.
                Add keywords.
                Make experience achievement based.
                """
            },

            {
                "role":"user",
                "content":resume
            }

        ]

    )


    return response.choices[0].message.content

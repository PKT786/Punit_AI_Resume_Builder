from openai import OpenAI
import streamlit as st


client = OpenAI(
api_key=st.secrets["OPENAI_API_KEY"]
)



def generate_summary(role,skills):


    response = client.chat.completions.create(

    model="gpt-4.1-mini",

    messages=[

    {
    "role":"user",
    "content":

f"""
Create ATS professional summary.

Role:
{role}

Skills:
{skills}

"""
    }

    ]

    )


    return response.choices[0].message.content

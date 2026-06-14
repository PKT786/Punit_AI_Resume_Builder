from openai import OpenAI
import streamlit as st



def get_openai_client():


    client = OpenAI(

        api_key=
        st.secrets["OPENAI_API_KEY"]

    )


    return client
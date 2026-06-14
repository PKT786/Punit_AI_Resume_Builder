from openai import OpenAI
import streamlit as st


def get_openai_client():

    api_key = st.secrets.get(
        "OPENAI_API_KEY"
    )


    if not api_key:

        raise Exception(
            "OPENAI_API_KEY not found in Streamlit secrets"
        )


    client = OpenAI(
        api_key=api_key
    )


    return client

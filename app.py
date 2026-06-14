import streamlit as st

from components.header import hero
from components.cards import feature_cards


st.set_page_config(
    page_title="AI Resume Builder",
    layout="wide"
)


hero()


feature_cards()


st.button(
    "🚀 Create New Resume"
)

st.button(
    "📤 Upload Resume"
)

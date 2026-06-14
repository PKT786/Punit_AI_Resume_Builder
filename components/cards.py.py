import streamlit as st


def feature_cards():

    col1,col2,col3,col4 = st.columns(4)


    with col1:

        st.success(
        """
        🤖 AI Optimization

        Improve content
        automatically
        """
        )


    with col2:

        st.info(
        """
        ATS Score

        Check recruiter
        compatibility
        """
        )


    with col3:

        st.warning(
        """
        Templates

        Modern
        ATS
        Developer
        """
        )


    with col4:

        st.error(
        """
        Export

        PDF + DOCX
        """
        )

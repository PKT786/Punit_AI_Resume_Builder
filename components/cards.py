import streamlit as st


def feature_cards():


    col1,col2,col3,col4 = st.columns(4)


    with col1:

        st.info(
        """
        🤖 AI Optimization

        Improve resume content
        using AI
        """
        )


    with col2:

        st.success(
        """
        🛡 ATS Friendly

        Recruiter ready format
        """
        )


    with col3:

        st.warning(
        """
        📄 Templates

        Modern
        ATS
        Developer
        """
        )


    with col4:

        st.error(
        """
        ⬇ Export

        PDF + Word
        """
        )

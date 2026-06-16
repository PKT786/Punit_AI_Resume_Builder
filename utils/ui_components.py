import streamlit as st
import os



ASSET_PATH = "assets"



def show_logo():

    logo = os.path.join(

        ASSET_PATH,

        "logo.png"

    )


    if os.path.exists(logo):

        st.image(

            logo,

            width=120

        )




def hero_section(
        image,
        title,
        subtitle
):


    img_path = os.path.join(

        ASSET_PATH,

        image

    )


    col1,col2 = st.columns(

        [1,1]

    )



    with col1:


        st.title(title)


        st.write(subtitle)



    with col2:


        if os.path.exists(img_path):


            st.image(

                img_path,

                use_container_width=True

            )



def feature_card(
        title,
        description,
        image
):


    img=os.path.join(

        ASSET_PATH,

        image

    )


    with st.container():


        if os.path.exists(img):

            st.image(

                img,

                width=100

            )


        st.subheader(title)


        st.write(description)
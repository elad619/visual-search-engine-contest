import streamlit as st

def draw_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/iUct1n3t.png);
                background-repeat: no-repeat;
                padding-top: 8px;
                background-position: 20px 25px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

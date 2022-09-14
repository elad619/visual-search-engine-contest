import os

from PIL import Image
import streamlit as st

from streamlit_utils.draw_logo import draw_logo
from streamlit_utils.streamlit_search import perform_search

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def search_main():
    # logo = Image.open("data/logo/logo-NLI-1.png")
    # st.image(logo, width=100)
    draw_logo()

    input_type = st.sidebar.radio("Search by", ("Text", "Image"))
    if input_type == "Text":
        query = st.sidebar.text_input("Enter Text Search")
    elif input_type == "Image":
        query = st.sidebar.file_uploader("Upload a Photo to Search", type="jpg")
    submit = st.sidebar.button("Search")
    if submit:
        st.empty()
        st.title("National Library Search Results:")
        if input_type == "Image":
            query = Image.open(query).convert('RGB')

        perform_search(query, input_type)
    else:
        st.write("")

    st.sidebar.markdown("***")
    st.sidebar.write("##")
    st.sidebar.write("##")


    st.sidebar.button("Have some fun with NLI images 🎨")


if __name__ == "__main__":
    search_main()

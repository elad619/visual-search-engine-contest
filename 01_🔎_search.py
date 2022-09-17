import os
import time

from PIL import Image
import streamlit as st

from image_creator.image_creator import have_fun_with_nli_images
from streamlit_utils.draw_logo import draw_logo
from streamlit_utils.streamlit_search import perform_search

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if 'button' not in st.session_state:
    st.session_state.button = False


def button_clicked():
    st.session_state.button = True


def search_main():
    # logo = Image.open("data/logo/logo-NLI-1.png")
    # st.image(logo, width=100)
    draw_logo()

    search_placeholder = st.sidebar.empty()

    with search_placeholder.container():
        input_type = st.radio("Search by", ("Text", "Image"))
        if input_type == "Text":
            query = st.text_input("Enter Text Search")
        elif input_type == "Image":
            query = st.file_uploader("Upload a Photo to Search", type="jpg")

        submit = st.button("Search")

        st.markdown("***")
        create_images_button = st.button("Have some fun with NLI images 🎨", on_click=button_clicked)

    if submit:
        st.empty()
        st.title("National Library Search Results:")
        if input_type == "Image":
            query = Image.open(query).convert('RGB')

        perform_search(query, input_type)
    else:
        st.write("")

    if create_images_button or st.session_state.button:
        search_placeholder.empty()
        have_fun_with_nli_images()


if __name__ == "__main__":
    search_main()

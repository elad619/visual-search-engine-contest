import os

from PIL import Image
import streamlit as st

from streamlit_utils.streamlit_search import perform_search

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if 'button' not in st.session_state:
    st.session_state.button = False

if "counter" not in st.session_state:
    st.session_state.counter = 1

if "similar_items_print_blocker" not in st.session_state:
    st.session_state.similar_items_print_blocker = False


def button_clicked():
    st.session_state.similar_items_print_blocker = True
    st.session_state.button = True


def search_main():
    # logo = Image.open("data/logo/logo-NLI-1.png")
    # st.image(logo, width=100)
    # draw_logo()

    st.sidebar.title("Yad Vashem - AI Image Search")

    search_placeholder = st.sidebar.empty()
    st.session_state.similar_items_print_blocker = False

    with search_placeholder.container():
        input_type = st.radio("Search by", ("Text", "Image"))
        if input_type == "Text":
            query = st.text_input("Enter Text Search")
        elif input_type == "Image":
            query = st.file_uploader("Upload a Photo to Search", type="jpg")

        matching_images_number_to_present = st.number_input(label="Top Images to Present", value=20, min_value=1,
                                                            max_value=100, step=1)

        submit = st.button("Search")

    if submit:
        st.empty()
        st.title("Yad Vashem Search Results:")
        if input_type == "Image":
            query = Image.open(query).convert('RGB')

        perform_search(query, input_type, matching_images_number_to_present)
    else:
        st.write("")


if __name__ == "__main__":
    search_main()

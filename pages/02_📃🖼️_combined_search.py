import os

from PIL import Image
import streamlit as st

from streamlit_utils.streamlit_search import perform_combined_search

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

    st.sidebar.title("Met - AI Image Search")

    search_placeholder = st.sidebar.empty()
    st.session_state.similar_items_print_blocker = False

    with search_placeholder.container():
        first_query_type = st.radio("Query 1 Type", ('Image', 'Text'))
        first_query_weight = st.number_input("Query 1 Weight", min_value=-1.0, max_value=1.0, value=0.5)
        if first_query_type == "Image":
            first_query = st.file_uploader("Upload a Photo to Search", type=["jpg", "png"], key="first_image_query")
        else:
            first_query = st.text_input("Enter Text Search", key="first_text_query")

        second_query_type = st.radio("Query 2 Type", ('Image', 'Text'))
        second_query_weight = st.number_input("Query 2 Weight", min_value=-1.0, max_value=1.0, value=0.5)
        if second_query_type == "Image":
            second_query = st.file_uploader("Upload a Photo to Search", type=["jpg", "png"], key="second_image_query")
        else:
            second_query = st.text_input("Enter Text Search", key="second_text_query")

        matching_images_number_to_present = st.number_input(label="Top Images to Present", value=20, min_value=1,
                                                            max_value=100, step=1)

        submit = st.button("Search")

    if submit:
        st.empty()
        st.title("Query:")
        search_queries_columns = st.columns(5)
        search_queries_columns[0].title(f"{first_query_weight}")

        if first_query_type == "Image":
            first_query = Image.open(first_query).convert('RGB')
            search_queries_columns[1].image(first_query, width=200)
        else:
            search_queries_columns[1].title(first_query)
        search_queries_columns[2].title("+")
        search_queries_columns[3].title(f"{second_query_weight}")

        if second_query_type == "Image":
            second_query = Image.open(second_query).convert('RGB')
            search_queries_columns[4].image(second_query, width=200)
        else:
            search_queries_columns[4].write(second_query)

        st.title("Met Search Results:")

        perform_combined_search(first_query, first_query_type, first_query_weight, second_query, second_query_type,
                                second_query_weight,matching_images_number_to_present)


if __name__ == "__main__":
    search_main()

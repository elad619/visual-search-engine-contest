import pandas as pd
from PIL import Image
import streamlit as st

from image_creator.image_creator import have_fun_with_nli_images
from streamlit_utils.draw_logo import draw_logo
from streamlit_utils.streamlit_search import perform_search

if 'button' not in st.session_state:
    st.session_state.button = False


def button_clicked():
    st.session_state.button = True


def similar_items_main(images_metadata):
    search_placeholder = st.sidebar.empty()
    if st.session_state.button:
        search_placeholder.empty()
        st.empty()
        have_fun_with_nli_images()
        return

    with search_placeholder.container():
        record_id_to_search = st.selectbox(
            'Choose NLI item record id:',
            reversed(images_metadata["record_id"].to_list()), key="1")
        item_size = images_metadata.loc[images_metadata["record_id"] == record_id_to_search, "size"].values[0]
        image_number_in_item = st.number_input('image number in item', value=1, max_value=item_size, min_value=1)

        image_identifier_to_search = images_metadata.loc[images_metadata["record_id"] == record_id_to_search,
                                                         "image_identifier"].values[0]

        submit = st.button("Search")

        st.markdown("***")
        create_images_button = st.button("get creative with NLI images 🎨", on_click=button_clicked)

    image_file_name = f"{image_identifier_to_search}-{int(image_number_in_item) - 1}"
    image_to_search = Image.open(f"data/images/{image_file_name}.jpg").convert('RGB')
    st.empty()
    st.header("You chose to search the following NLI image:")
    st.image(image_to_search, width=500)
    st.write(" ")

    if submit:

        st.header("Similar NLI images:")
        perform_search(image_to_search, "Image", is_closest_item_search=True)
    else:
        st.write("")

    if create_images_button or st.session_state.button:
        search_placeholder.empty()
        st.empty()
        have_fun_with_nli_images()


if __name__ == "__main__":
    draw_logo()
    images_metadata = pd.read_csv("data/images/metadata/images_metadata.csv")
    similar_items_main(images_metadata)

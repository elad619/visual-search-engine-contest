import pandas as pd
from PIL import Image
import streamlit as st

from streamlit_utils.draw_logo import draw_logo
from streamlit_utils.streamlit_search import perform_search


def similar_items_main(images_metadata):
    record_id_to_search = st.sidebar.selectbox(
        'Choose NLI item record id:',
        reversed(images_metadata["record_id"].to_list()))
    item_size = images_metadata.loc[images_metadata["record_id"] == record_id_to_search, "size"].values[0]
    image_number_in_item = st.sidebar.number_input('image number in item', value=1, max_value=item_size)

    image_identifier_to_search = images_metadata.loc[images_metadata["record_id"] == record_id_to_search,
                                                     "image_identifier"].values[0]

    image_file_name = f"{image_identifier_to_search}-{image_number_in_item - 1}"

    submit = st.sidebar.button("Search")
    if submit:
        image_to_search = Image.open(f"data/images/{image_file_name}.jpg").convert('RGB')
        st.empty()
        st.header("You chose to search the following NLI image:")
        st.image(image_to_search, width=500)
        st.write(" ")

        st.header("Similar NLI images:")
        perform_search(image_to_search, "Image", is_closest_item_search=True)
    else:
        st.write("")


if __name__ == "__main__":
    draw_logo()
    images_metadata = pd.read_csv("data/images/metadata/images_metadata.csv")
    similar_items_main(images_metadata)

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from bokeh.models.widgets import Div

from nli_searcher import searcher
from utils.met_reader.met_reader import read_image_from_local
from utils.s3_reader.s3_reader import read_image_from_s3

features_path = Path("data/features")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
nli_search_url = "https://merhav.nli.org.il/primo-explore/search?query=any,contains,{photo_search_identifier}&sortby=rank&vid=NLI&lang=iw_IL"

images_metadata = pd.read_csv("data/metadata/metadata.csv")


def scroll_to_page_top():
    components.html(
        f"""
            <p>{st.session_state.counter}</p>
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
        """,
        height=0
    )
    st.session_state.counter += 1


def nav_to(url):
    js = f"window.location.href = '{url}'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)


def find_similar(image_to_search):
    st.session_state.similar_items_print_blocker = True
    scroll_to_page_top()
    st.empty()
    st.header("You chose to search the following Met image:")
    st.image(image_to_search, width=500)
    st.write(" ")
    st.header("Similar Met images:")
    perform_normal_search(image_to_search, "Image", is_closest_item_search=True)


def perform_combined_search(first_query, first_query_type, first_query_weight, second_query, second_query_type,
                            second_query_weight, matching_images_number_to_present, is_closest_item_search=False):
    best_photos = searcher.search_combined(first_query, first_query_type, first_query_weight,
                                           second_query,
                                           second_query_type,
                                           second_query_weight)
    # Iterate over the top 3 results
    search_range = range(matching_images_number_to_present)
    for i in search_range:
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]

        # Display the photo
        image = read_image_from_local(photo_id)
        # photo_search_identifiers = photo_id.split('-')[0]
        # image_docID_seperated = photo_search_identifiers.split('_')[:-1]
        # image_docID = '_'.join(image_docID_seperated)
        #
        # image_nli_url = nli_search_url.format(photo_search_identifier=image_docID)
        st.image(image, width=500)
        columns = st.columns(2)

        find_similar_button = columns[0].button("find similar images 🖼️☝️ ", on_click=find_similar,
                                                kwargs=dict(image_to_search=image),
                                                key=(str(i) + str(is_closest_item_search)))

        # columns[1].button('more info ℹ️', on_click=nav_to, kwargs=dict(url=image_nli_url),
        #                   key=(str(i) + str(is_closest_item_search) + "info"))

        if photo_id in images_metadata['filename'].values:
            image_description = images_metadata[images_metadata['filename'] == photo_id]['title'].values[0]
            image_category = images_metadata[images_metadata['filename'] == photo_id]['category'].values[0]
            st.write(f"description☝️ : {image_description}")
            st.write(f"category☝️ : {image_category}")
        st.markdown("---")


def perform_normal_search(query, input_type, matching_images_number_to_present=20, is_closest_item_search=False):
    best_photos = searcher.search_image_or_text(query, input_type)
    # Iterate over the top 3 results
    search_range = range(matching_images_number_to_present)
    for i in search_range:
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]

        # Display the photo
        image = read_image_from_local(photo_id)
        # photo_search_identifiers = photo_id.split('-')[0]
        # image_docID_seperated = photo_search_identifiers.split('_')[:-1]
        # image_docID = '_'.join(image_docID_seperated)
        #
        # image_nli_url = nli_search_url.format(photo_search_identifier=image_docID)
        st.image(image, width=500)
        columns = st.columns(2)

        find_similar_button = columns[0].button("find similar images 🖼️☝️ ", on_click=find_similar,
                                                kwargs=dict(image_to_search=image),
                                                key=(str(i) + str(is_closest_item_search)))

        # columns[1].button('more info ℹ️', on_click=nav_to, kwargs=dict(url=image_nli_url),
        #                   key=(str(i) + str(is_closest_item_search) + "info"))

        if photo_id in images_metadata['filename'].values:
            image_description = images_metadata[images_metadata['filename'] == photo_id]['title'].values[0]
            image_category = images_metadata[images_metadata['filename'] == photo_id]['category'].values[0]
            st.write(f"description☝️ : {image_description}")
            st.write(f"category☝️ : {image_category}")
        st.markdown("---")

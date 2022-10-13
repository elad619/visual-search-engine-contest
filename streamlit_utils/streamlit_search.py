from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
from bokeh.models.widgets import Div

from nli_searcher import searcher

features_path = Path("data/features")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
nli_search_url = "https://merhav.nli.org.il/primo-explore/search?query=any,contains,{photo_search_identifier}&sortby=rank&vid=NLI&lang=iw_IL"



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
    st.header("You chose to search the following NLI image:")
    st.image(image_to_search, width=500)
    st.write(" ")
    st.header("Similar NLI images:")
    perform_search(image_to_search, "Image", is_closest_item_search=True)


def perform_search(query, input_type, is_closest_item_search=False):
    best_photos = searcher.search_nli(query, input_type)
    # Iterate over the top 3 results
    search_range = range(1, 6) if is_closest_item_search else range(3)
    for i in search_range:
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]

        # Display the photo
        image = Image.open(f"./data/images/{photo_id}.jpg")
        photo_search_identifiers = photo_id.split('-')[0]
        image_docID_seperated = photo_search_identifiers.split('_')[:-1]
        image_docID = '_'.join(image_docID_seperated)

        image_nli_url = nli_search_url.format(photo_search_identifier=image_docID)
        st.image(image, width=500)
        columns = st.columns(2)

        find_similar_button = columns[0].button("find similar images 🖼️☝️ ", on_click=find_similar,
                                                kwargs=dict(image_to_search=image),
                                                key=(str(i) + str(is_closest_item_search)))

        columns[1].button('more info ℹ️', on_click=nav_to, kwargs=dict(url=image_nli_url),
                          key=(str(i) + str(is_closest_item_search) + "info"))
        st.write(" ")
        st.write(" ")

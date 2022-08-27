from pathlib import Path

import streamlit as st
import pandas as pd
from PIL import Image

from nli_searcher import searcher

features_path = Path("data/features")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
nli_search_url = "https://merhav.nli.org.il/primo-explore/search?query=any,contains,{photo_search_identifier}&sortby=rank&vid=NLI&lang=iw_IL"


def perform_search(query, input_type, is_closest_item_search=False):
    best_photos = searcher.search_nli(query, input_type)
    # Iterate over the top 3 results
    search_range = range(1, 4) if is_closest_item_search else range(3)
    for i in search_range:
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]

        # Display the photo
        image = Image.open(f"./data/images/{photo_id}.jpg")
        photo_search_identifiers = photo_id.split('-')[0]
        image_docID_seperated = photo_search_identifiers.split('_')[:-1]
        image_docID = '_'.join(image_docID_seperated)

        image_url = nli_search_url.format(photo_search_identifier=image_docID)
        link = f'check ☝️ image on [National Library\'s Website]({image_url})'
        st.image(image, width=500)
        st.markdown(link, unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")

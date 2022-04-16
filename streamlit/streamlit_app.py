import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from nli_searcher import searcher


import streamlit as st


features_path = Path(r"./data/features")
# Load the features and the corresponding IDs
photo_features = np.load(features_path / "features.npy")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
nli_search_url = "https://merhav.nli.org.il/primo-explore/search?query=any,contains,{photo_search_identifier}&sortby=rank&vid=NLI&lang=iw_IL"


def perform_search(query, input_type):
    best_photos = searcher.search_nli(query, input_type)
    # Iterate over the top 3 results
    for i in range(3):
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]

        # Display the photo
        image = Image.open(f".\\data\\images\\{photo_id}\\{photo_id}.jpg")
        photo_search_identifier = re.findall("[0-9]+", photo_id)[0]
        image_url = nli_search_url.format(photo_search_identifier=photo_search_identifier)
        link = f'check ☝️ image on [National Library\'s Website]({image_url})'
        st.image(image)
        st.markdown(link, unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")


def main():
    logo = Image.open(".\\data\\logo\\logo-NLI-1.png")
    st.sidebar.title("Visual Search Engine")
    st.sidebar.image(logo, width=250)

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


if __name__ == "__main__":
    main()

import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
from nli_searcher import searcher

features_path = Path("./data/features")
# Load the features and the corresponding IDs
photo_features = np.load(features_path / "features.npy")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
nli_search_url = "https://www.nli.org.il/he/search?projectName=NLI#&q=any,contains,{photo_search_identifier}&bulkSize=30&index=0&sort=rank&t=allresults"


def perform_search(query, input_type):
    best_photos = searcher.search_nli(query, input_type)
    # Iterate over the top 3 results
    for i in range(3):
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
        st.image(image)
        st.markdown(link, unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")


def main():
    logo = Image.open("./data/logo/logo-NLI-1.png")
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

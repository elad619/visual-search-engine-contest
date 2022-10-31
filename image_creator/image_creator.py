import os
import time

import replicate
import streamlit as st
import pandas as pd
from PIL import Image

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
model = replicate.models.get("stability-ai/stable-diffusion")
model = model.versions.get("a826166bdfbd1c12981a2e914120aa8c19ab2b5474ff8c70f4e2923e6d6596cc")

images_metadata = pd.read_csv("data/images/metadata/images_metadata.csv")


def back_button():
    st.session_state.button = False


def create_image(original_image_file, prompt, prompt_strength, guidance_scale):
    new_images = model.predict(prompt=prompt,
                               width=768,
                               height=512,
                               num_inference_steps=70,
                               init_image=original_image_file,
                               prompt_strength=prompt_strength,
                               guidance_scale=guidance_scale,
                               num_outputs=4)
    st.title("New images")
    cols = st.columns(2)

    for i, image in enumerate(new_images):
        cols[i % 2].image(image, width=256)


def have_fun_with_nli_images():
    end_button = st.sidebar.button("Back to search engine 🔙", on_click=back_button)
    st.sidebar.markdown("###")

    record_id_to_search = st.sidebar.selectbox(
        'Choose NLI item record id:',
        reversed(images_metadata["record_id"].to_list()), key="2")
    item_size = images_metadata.loc[images_metadata["record_id"] == record_id_to_search, "size"].values[0]
    image_number_in_item = st.sidebar.number_input('image number in item', value=1, max_value=item_size, key="3",
                                                   min_value=1)
    image_identifier_to_edit = images_metadata.loc[images_metadata["record_id"] == record_id_to_search,
                                                   "image_identifier"].values[0]

    image_file_name = f"{image_identifier_to_edit}-{image_number_in_item - 1}"

    if "." in image_file_name:
        image_file_name = image_file_name.split(".")[0]

    original_image_file = open(f"data/images/{image_file_name}.jpg", "rb")

    prompt = st.sidebar.text_input("Enter a text prompt")

    prompt_strength = st.sidebar.slider("How much to change the image", min_value=0.0, max_value=1.0,
                                        value=0.5)
    guidance_scale = st.sidebar.slider("Text strength", min_value=0.0, max_value=20.0, value=7.5)

    image_to_edit_for_display = Image.open(f"data/images/{image_file_name}.jpg").convert('RGB')

    st.title("Original image")
    st.image(image_to_edit_for_display, width=512)

    button = st.sidebar.button("Edit NLI image 🎨")
    if button:
        with st.spinner('Wait for it...'):
            create_image(original_image_file, prompt, prompt_strength, guidance_scale)

    st.sidebar.markdown("***")


if __name__ == "__main__":
    have_fun_with_nli_images()

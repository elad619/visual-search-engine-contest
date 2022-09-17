import os

import replicate
import streamlit as st
import pandas as pd
from PIL import Image

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
model = replicate.models.get("stability-ai/stable-diffusion")
images_metadata = pd.read_csv("data/images/metadata/images_metadata.csv")


def create_image(original_image_file, prompt, prompt_strength, guidance_scale):
    new_image = model.predict(prompt=prompt,
                              width=512,
                              height=512,
                              num_inference_steps=100,
                              init_image=original_image_file,
                              prompt_strength=prompt_strength,
                              guidance_scale=guidance_scale)
    st.title("New image")
    st.image(new_image, width=512)


def have_fun_with_nli_images():
    record_id_to_search = st.sidebar.selectbox(
        'Choose NLI item record id:',
        reversed(images_metadata["record_id"].to_list()), key="2")
    item_size = images_metadata.loc[images_metadata["record_id"] == record_id_to_search, "size"].values[0]
    image_number_in_item = st.sidebar.number_input('image number in item', value=1, max_value=item_size, key="3")

    image_identifier_to_edit = images_metadata.loc[images_metadata["record_id"] == record_id_to_search,
                                                   "image_identifier"].values[0]

    image_file_name = f"{image_identifier_to_edit}-{image_number_in_item - 1}"
    original_image_file = open(f"data/images/{image_file_name}.jpg", "rb")

    prompt = st.sidebar.text_input("Enter a prompt")

    prompt_strength = st.sidebar.slider("How much to change the image", min_value=0.0, max_value=1.0,
                                        value=0.5)
    guidance_scale = st.sidebar.slider("Text strength", min_value=0.0, max_value=20.0, value=7.5)

    image_to_edit_for_display = Image.open(f"data/images/{image_file_name}.jpg").convert('RGB')

    st.title("Original image")
    st.image(image_to_edit_for_display, width=512)

    button = st.sidebar.button("Create new image 🎨")
    if button:
        with st.spinner('Wait for it...'):
            create_image(original_image_file, prompt, prompt_strength, guidance_scale)

    st.sidebar.markdown("***")
    end_button = st.sidebar.button("Finish Editing 🔙")
    if end_button:
        st.session_state.button = False


if __name__ == "__main__":
    have_fun_with_nli_images()

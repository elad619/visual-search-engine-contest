import io

import streamlit as st
import s3fs
from PIL import Image

BUCKET_NAME = 'yad-vashem-ai-search-engine'

fs = s3fs.S3FileSystem(anon=False)


def read_image_from_s3(photo_id):
    with fs.open(f's3://{BUCKET_NAME}/images/{photo_id}.jpg') as f:
        image = Image.open(io.BytesIO(f.read()))
    return image

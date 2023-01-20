from pathlib import Path

import numpy as np
import pandas as pd
import torch

# Set the paths
from model.clip import clip

features_path = Path(r"./data/features")
# Load the features and the corresponding IDs
photo_features = np.load(features_path / "features.npy")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)


# image_model = CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32")
# image_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def search_by_text_and_photo(text_query, image_query, image_weight=0.5):
    with torch.no_grad():
        text_encoded = model.encode_text(clip.tokenize(text_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)

    with torch.no_grad():
        # inputs = image_processor(images=search_query, return_tensors="pt")
        # outputs = image_model(**inputs)
        image = preprocess(image_query).unsqueeze(0).to(device)
        image_encoded = model.encode_image(image)
        image_encoded /= image_encoded.norm(dim=-1, keepdim=True)

    search_features = text_encoded + image_encoded * image_weight
    search_features /= search_features.norm(dim=-1, keepdim=True)

    # Retrieve the description vector and the photo vectors
    features = search_features.cpu().numpy()

    # Compute the similarity between the descrption and each photo using the Cosine similarity
    similarities = list((features @ photo_features.T).squeeze(0))

    # Sort the photos by their similarity score
    best_photos = sorted(zip(similarities, range(photo_features.shape[0])), key=lambda x: x[0], reverse=True)
    return best_photos


def search_image_or_text(search_query, query_type):
    if query_type == "Text":
        with torch.no_grad():
            input_encoded = model.encode_text(clip.tokenize(search_query).to(device))

    elif query_type == "Image":
        with torch.no_grad():
            # inputs = image_processor(images=search_query, return_tensors="pt")
            # outputs = image_model(**inputs)
            image = preprocess(search_query).unsqueeze(0).to(device)
            input_encoded = model.encode_image(image)

    input_encoded /= input_encoded.norm(dim=-1, keepdim=True)

    # Retrieve the description vector and the photo vectors
    features = input_encoded.cpu().numpy()

    # Compute the similarity between the descrption and each photo using the Cosine similarity
    similarities = list((features @ photo_features.T).squeeze(0))

    # Sort the photos by their similarity score
    best_photos = sorted(zip(similarities, range(photo_features.shape[0])), key=lambda x: x[0], reverse=True)
    return best_photos

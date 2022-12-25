from pathlib import Path
import os

import numpy as np
import pandas as pd
from nli_searcher import searcher

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

features_path = Path("data/features")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])

MATCHING_IMAGES_NUMBER_TO_PRESENT = 20

def get_ids_from_engine(text_query):
    best_photos = searcher.search_nli(text_query, "Text")
    similar_images_identifiers = [photo_ids[best_photos[i][1]] for i in range(MATCHING_IMAGES_NUMBER_TO_PRESENT)]
    return similar_images_identifiers

def measure_item_search(image_row):
    similar_images_identifiers = get_ids_from_engine(image_row["title"])
    return image_row["filename"] in similar_images_identifiers

def measure_category_images(images_metadata,category):
    category_images = images_metadata[images_metadata["category"] == category]
    category_search_results = np.array(get_ids_from_engine(category))
    intersection = np.intersect1d(category_images["filename"].values, category_search_results)
    return intersection.shape[0]


def measure_categories():
    images_metadata = pd.read_csv("data/metadata/metadata.csv")
    categories = images_metadata["category"].unique()
    for category in categories:
        category_search_intersection = measure_category_images(images_metadata,category)
        print(f"{category}: {category_search_intersection}")


def measure_by_title_search(images_metadata):
    images_metadata["is_caught_by_engine"] = images_metadata.apply(measure_item_search, axis=1)
    images_caught_by_engine = images_metadata[images_metadata["is_caught_by_engine"] == True]
    print(f"caught by engine: {images_caught_by_engine.shape[0]}")

    images_not_caught_by_engine = images_metadata[images_metadata["is_caught_by_engine"] == False]
    print(f"not caught by engine: {images_not_caught_by_engine.shape[0]}")

    print(f"caught by engine percentage: {images_caught_by_engine.shape[0] / (images_caught_by_engine.shape[0]+images_not_caught_by_engine.shape[0])}")


if __name__ == "__main__":
    images_metadata = pd.read_csv("data/metadata/metadata.csv")
    images_metadata = images_metadata[images_metadata["title"].str.len() < 280]

    print("all images")
    measure_by_title_search(images_metadata)


    print("without kids and rabbis")

    images_metadata = images_metadata[images_metadata["category"] != "youngsters"]
    images_metadata = images_metadata[images_metadata["category"] != "children"]
    images_metadata = images_metadata[images_metadata["category"] != "Rabbis"]

    measure_by_title_search(images_metadata)
    #images_metadata.to_csv("images_metadata.csv", index=False)

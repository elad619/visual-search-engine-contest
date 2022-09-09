from pathlib import Path
import os


import pandas as pd
from nli_searcher import searcher

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


features_path = Path("data/features")
photo_ids = pd.read_csv(features_path / "photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])


def measure_item_search(image_row):
    best_photos = searcher.search_nli(image_row["description"], "Text")
    similar_images_identifiers = [photo_ids[best_photos[i][1]].split("-")[0] for i in range(3)]
    return image_row["image_identifier"] in similar_images_identifiers



if __name__ == "__main__":
    images_metadata = pd.read_csv("utils/images_metadata.csv")
    images_with_good_description = images_metadata[images_metadata["collection_type"] != "manuscript"]

    images_with_good_description["is_caught_by_engine"] = images_with_good_description.apply(measure_item_search,axis=1)
    print(images_with_good_description["is_caught_by_engine"].value_counts())

    #images_metadata.to_csv("images_metadata.csv", index=False)

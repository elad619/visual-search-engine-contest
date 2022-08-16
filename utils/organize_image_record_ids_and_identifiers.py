import pandas as pd

from utils.image_downloader import get_image_identifiers, get_image_record_id


def get_image_identifier_from_nli(image_row):
    docID, ie = get_image_identifiers(image_row["id"], image_row["collection_type"])
    image_identifier = f'{docID}_{ie}'
    return image_identifier


def get_image_record_id_from_nli(image_row):
    image_docID_seperated = image_row["id"].split('_')[:-1]
    image_docID = '_'.join(image_docID_seperated)
    record_id = get_image_record_id(image_docID, image_row["collection_type"])
    return record_id


if __name__ == "__main__":
    images_db = pd.read_csv("new_images_database.csv")
    new_images_db = images_db[images_db["database_version"] == "new"]
    new_images_db["record_id"] = new_images_db["id"]
    new_images_db["image_identifier"] = new_images_db.apply(get_image_identifier_from_nli, axis=1)

    original_images_db = images_db[images_db["database_version"] == "original"]
    original_images_db["image_identifier"] = original_images_db["id"]
    original_images_db["record_id"] = original_images_db.apply(get_image_record_id_from_nli, axis=1)

    organized_images_db = pd.concat([new_images_db, original_images_db])
    organized_images_db = organized_images_db.drop(columns=['id'])
    organized_images_db.to_csv("organized_images_db.csv", index=False)

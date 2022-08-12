import pandas as pd

from utils.image_downloader import download_image

if __name__ == "__main__":
    images_db = pd.read_csv("images_db.csv")
    images_db = images_db[images_db["database_version"] == "new"]
    images_db.apply(lambda image_row: download_image(image_row["id"], image_row["collection_type"]), axis=1)

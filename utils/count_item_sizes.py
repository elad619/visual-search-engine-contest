import pandas as pd
import fnmatch,os

images_directory_path = "../data/images"
def calculate_item_size(image_identifier):
    num_files = len(fnmatch.filter(os.listdir(images_directory_path), f'{image_identifier}*'))
    return num_files


if __name__ == "__main__":
    images_metadata = pd.read_csv("images_metadata.csv")

    images_metadata["size"] = images_metadata["image_identifier"].apply(calculate_item_size)

    images_metadata.to_csv("images_metadata.csv", index=False)

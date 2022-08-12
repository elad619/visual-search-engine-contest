import shutil
from pathlib import Path


if __name__ == "__main__":
    photos_path = Path(r"C:\Users\elad6\OneDrive\Documents\NLI\images_db\raw\unzipped")

    # List all JPGs in the folder
    photos_files = list(photos_path.rglob("*.jpg"))

    for file_name in photos_files:
        shutil.copy(file_name, r"C:\Users\elad6\OneDrive\Documents\NLI\images_db\images")

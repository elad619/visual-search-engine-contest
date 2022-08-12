import ntpath
import os

path = r"C:\Users\elad6\OneDrive\Documents\NLI\images_db\raw\unzipped"

if __name__ == "__main__":
    # recursively walk through the directory to find folders
    for root, dir, files in os.walk(path):
        # walk through the folders to find files
        for file_index_in_folder, file in enumerate(files):
            dirname = ntpath.basename(root)
            ori = root + '/' + file
            name, file_extension = os.path.splitext(file)

            dest = f"{root}/{dirname}-{file_index_in_folder}{file_extension}"
            os.rename(ori, dest)

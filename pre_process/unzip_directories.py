
if __name__ == '__main__':
    import glob
    import os
    import zipfile

    zip_files = glob.glob('*.zip')
    os.mkdir("unzipped")

    for zip_filename in zip_files:
        dir_name = os.path.splitext(zip_filename)[0]
        created_unzipped_directory = f"unzipped\\{dir_name}"
        os.mkdir(created_unzipped_directory)
        zip_handler = zipfile.ZipFile(zip_filename, "r")
        zip_handler.extractall(created_unzipped_directory)

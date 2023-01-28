from PIL import Image

local_path = r"C:\Users\elad6\Documents\Billions of Words\imet\train"


def read_image_from_local(photo_id):
    image = Image.open(f"{local_path}/{photo_id}.png")
    return image

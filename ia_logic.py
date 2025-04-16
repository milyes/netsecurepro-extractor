from PIL import Image

def analyze_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        if width < 100 or height < 100:
            return "Image trop petite - possible anomalie"
        else:
            return "Image analysée - OK"

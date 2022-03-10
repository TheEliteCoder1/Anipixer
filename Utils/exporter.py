from PIL import Image

def new_image():
    img = Image.new('RGB', (285, 285))
    img.putpixel((30,60), (155,155,55))
    img.save('sqr.png')
from PIL import Image
from .colors import COLORS
import random

def new_image(width, height, grid):
    print(len(grid) / height)
    # img = Image.new('RGB', (width, width*height))
    # for x in range(width):
    #     for y in range(height):
    #         print(x*px_size)
    #         img.putpixel((x*px_size, y*px_size), random.choice(list(COLORS.values())))
    # img.save(path)

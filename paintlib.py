from Utils import colors
from Gui.depends import *
import collections

# Application Cursor
CURSORS = {
    "pointer":"UI/Cursors/ubuntu-pointer.png",
    "black_pointer":"UI/Cursors/black-pointer.png",
    "eraser":"UI/Cursors/eraser.png",
    "line":"UI/Cursors/line.png"
}

# BASIC Colors as seperate variables (Just For Convienience, but is also a pallete)
BLACK = colors.COLORS["black"]
WHITE = colors.COLORS["white"]
YELLOW = colors.COLORS["yellow1"]
RED = colors.COLORS["red1"]
PURPLE = colors.COLORS["purple"]
BLUE = colors.COLORS["blue"]
BROWN = colors.COLORS["brick"]
GREEN  = colors.COLORS["green1"]

FONTS = {
    "ui_font":"UI/Fonts/proxima_nova.ttf",
    "ui_thick_font":"UI/Fonts/opensans_extrabold.ttf"
}

"""Color Dictionary containing all colors availible."""
colors_dict = {}
for letter in colors.ALPHABET:
    value = {color:colors.COLORS[color] for color in colors.get_names_list() if color.startswith(letter)}
    if len(value) > 0: # if the color has an actual letter group, then record the value.
        colors_dict[f"{letter}"] = value # creates all availible palletes based on first letter.

# Adding Special Groups -> Basic Colors
# Custom pallete names are new dictionary assignments to color_dict.
colors_dict["basic_colors"] = {
    "black":colors.COLORS["black"],
    "white":colors.COLORS["white"],
    "yellow":colors.COLORS["yellow1"],
    "red":colors.COLORS["red1"],
    "purple":colors.COLORS["purple"],
    "blue":colors.COLORS["blue"],
    "brown":colors.COLORS["brick"],
    "green":colors.COLORS["green1"]
}
# Ordering the position of each color alphabeticaly with first character rule.
colors_dict["basic_colors"] = collections.OrderedDict(sorted(colors_dict["basic_colors"].items()))

# Used when created color palletes.
basic_colors_list = [color for (name, color) in colors_dict['basic_colors'].items()]

def print_colors_dict():
    """Formatted Output of all colors, rgb values, and thier groups/palletes."""
    for color_group in colors_dict.keys():
        for color_name, rgb in colors_dict[color_group].items():
            print(color_group, color_name, rgb)
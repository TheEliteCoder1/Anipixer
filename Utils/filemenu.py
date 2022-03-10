"""Handles all file load, read, and save operations in Anipixer."""
# Anipixer working files: (*.anp)
# .anp files are similar to JSON syntax.
from Gui.depends import pygame
from .utils import load_json_data, save_json_data


def save_canvas_to_anp(canvas, filename):
    """Saves Anipixer work as a working file (*.anp)"""
    # getting canvas data from canvas grid
    canvas_data = []
    for i in range(len(canvas.grid)):
        pixel = (canvas.grid[i]["pixel"].x, canvas.grid[i]["pixel"].y, canvas.grid[i]["pixel"].width, canvas.grid[i]["pixel"].height)
        color = canvas.grid[i]["color"]
        canvas_data.append({"color":color, "pixel":pixel})        
    # all of the working file data needed to save.
    file_data = {
        "canvas_data":canvas_data
    }
    # Saving Canvas Data
    save_json_data(filename, file_data)

def open_canvas_from_anp(filename):
    """Returns the grid of of a canvas from an anp."""
    canvas_data = load_json_data(filename)['canvas_data']
    for i in range(len(canvas_data)):
        canvas_data[i]["pixel"] = pygame.Rect(*canvas_data[i]["pixel"])
    return canvas_data
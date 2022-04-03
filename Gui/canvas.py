from .depends import *
from Utils.colors import COLORS

class Canvas:
    """Representation of a Pixel Art Canvas."""
    def __init__(self, screen, x, y, width, height, pixel_size, grid):
        self.screen = screen
        self.x = x - x/2
        self.y = y
        self.width = width
        self.height = height
        self.canvas_color = (255,255,255)
        self.drawing_color = COLORS["black"]
        self.pixel_size = pixel_size
        self.max_version_saves = 10
        self.copied = False
        self.hovering_color_swatch = None
        # Initializing the grid
        self.grid = grid # contains all the data on the canvas, including drawn pixels.
        if len(self.grid) < 1: # if empty than fill white
            for x in range(self.width):
                for y in range(self.height):
                    pixel = pygame.Rect(x*self.pixel_size+self.x, y*self.pixel_size+self.y, self.pixel_size, self.pixel_size)
                    self.grid.append({"pixel":pixel, "color":self.canvas_color})
        self.selected_pixels = []
        self.copied_pixels = []
        self.initial_grid = self.grid # recovers original grid with no changes saved.
        self.canvas_boundary = pygame.Rect(*self.grid[0]["pixel"].topleft, self.width*self.pixel_size, self.height*self.pixel_size)

    def change_data(self, grid):
        self.grid = grid # contains all the data on the canvas, including drawn pixels.
        if len(self.grid) < 1: # if empty than fill white
            for x in range(self.width):
                for y in range(self.height):
                    pixel = pygame.Rect(x*self.pixel_size+self.x, y*self.pixel_size+self.y, self.pixel_size, self.pixel_size)
                    self.grid.append({"pixel":pixel, "color":self.canvas_color})
        self.selected_pixels = []
        self.copied_pixels = []
        self.initial_grid = self.grid # recovers original grid with no changes saved.
        self.canvas_boundary = pygame.Rect(*self.grid[0]["pixel"].topleft, self.width*self.pixel_size, self.height*self.pixel_size)   
        
    def draw(self, grid, canvas_boundary, show_grid, select_mode):
        """Draws the Canvas to the screen every frame."""
        # Drawing Canvas
        for pixel in grid:
            if show_grid == False:
                pygame.draw.rect(self.screen, pixel["color"], pixel["pixel"])
            elif show_grid == True:
                pygame.draw.rect(self.screen, pixel["color"], pixel["pixel"])
                pygame.draw.rect(self.screen, COLORS["black"], pixel["pixel"], width=1)
        # Draw Canvas Boundary
        pygame.draw.rect(self.screen, COLORS["black"], canvas_boundary, width=1)

        # Draw selected pixels
        if select_mode == True:
            for pixel in self.selected_pixels:
                pygame.draw.rect(self.screen, pixel["color"], pixel["pixel"])
                pygame.draw.rect(self.screen, COLORS["darkturquoise"], pixel["pixel"], width=1)

    def paint_pixel(self, mpos):
        """Checks if the mouse clicked any of the pixels on the grid, 
        and if so apply the selected drawing color to the pixel."""
        for i in range(len(self.grid)):
            if self.grid[i]["pixel"].collidepoint(mpos):
                self.grid[i]["color"] = self.drawing_color

    def select_pixels(self, mpos):
        """Selects pixels on the grid."""
        for i in range(len(self.grid)):
            if self.grid[i]["pixel"].collidepoint(mpos):
                selected_pixel = {"pixel":self.grid[i]["pixel"], "color":self.grid[i]["color"], "index":i} # we will also need the pixel's index on the grid for later.
                self.selected_pixels.append(selected_pixel)

    def move_copied_pixels(self, direction):
        """Moves the copied pixels using arrow keys."""
        if direction == 'up':
            for pixel in self.selected_pixels:
                try:
                    if pixel["index"]-1 >= 0 and pixel["index"]-1 <= len(self.grid):
                        pixel["pixel"] = self.grid[pixel["index"]-1]["pixel"]
                        pixel["index"] = pixel["index"]-1
                except:
                    pass
        elif direction == 'down':
            for pixel in self.selected_pixels:
                try:
                    if pixel["index"]+1 >= 0 and pixel["index"]+1 <= len(self.grid):
                        pixel["pixel"] = self.grid[pixel["index"]+1]["pixel"]
                        pixel["index"] = pixel["index"]+1
                except:
                    pass
        elif direction == 'right':
            for pixel in self.selected_pixels:
                try:
                    if pixel["index"]+self.height >= 0 and pixel["index"]+self.height <= len(self.grid):
                        pixel["pixel"] = self.grid[pixel["index"]+self.height]["pixel"]
                        pixel["index"] = pixel["index"]+self.height
                except:
                    pass
        elif direction == 'left':
            for pixel in self.selected_pixels:
                try:
                    if pixel["index"]-self.height >= 0 and pixel["index"]-self.height <= len(self.grid):
                        pixel["pixel"] = self.grid[pixel["index"]-self.height]["pixel"]
                        pixel["index"] = pixel["index"]-self.height
                except:
                    pass
                


    def copy_from_clipboard(self):
        """Copies the pixels in the clipboard."""
        self.copied = True

    def paste_from_clipboard(self):
        """Pastes the pixels in the clipboard."""
        for pixel in self.selected_pixels:
            self.grid[pixel["index"]] = {"pixel":pixel["pixel"], "color":pixel["color"]}

    def unselect_from_clipboard(self):
        """Unselects the pixels in the clipboard."""
        self.selected_pixels.clear()
                
    def clear_canvas(self):
        """Resets the pixel colors on the canvas."""
        for i in range(len(self.grid)):
            self.grid[i]["color"] = self.canvas_color    

    def undo(self):
        """Returns the last known saved version of the canvas."""
        pass

    def reset(self):
        """Resets canvas to the inital state when opened."""
        self.grid = self.initial_grid
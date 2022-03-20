from .depends import *
from Utils.colors import COLORS

class Canvas:
    """Representation of a Pixel Art Canvas."""
    def __init__(self, screen, x, y, width, height, pixel_size, grid):
        self.screen = screen
        self.x = x - x/2
        self.y = y
        self.undo_count = 0
        self.width = width
        self.height = height
        self.canvas_color = (255,255,255)
        self.drawing_color = COLORS["black"]
        self.pixel_size = pixel_size
        self.hovering_color_swatch = None
        # Initializing the grid
        self.grid = grid # contains all the data on the canvas, including drawn pixels.
        if len(self.grid) < 1: # if empty than fill white
            for x in range(self.width):
                for y in range(self.height):
                    pixel = pygame.Rect(x*self.pixel_size+self.x, y*self.pixel_size+self.y, self.pixel_size, self.pixel_size)
                    self.grid.append({"pixel":pixel, "color":self.canvas_color})
        self.initial_grid = self.grid # recovers original grid with no changes saved.
        self.previous_grids = [] # save previous versions
        self.canvas_boundary = pygame.Rect(*self.grid[0]["pixel"].topleft, self.width*self.pixel_size, self.height*self.pixel_size)    
        
    def draw(self, grid, canvas_boundary, show_grid):
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

    def paint_pixel(self, mpos):
        """Checks if the mouse clicked any of the pixels on the grid, 
        and if so apply the selected drawing color to the pixel."""
        for i in range(len(self.grid)):
            if self.grid[i]["pixel"].collidepoint(mpos):
                self.grid[i]["color"] = self.drawing_color

    def clear_canvas(self):
        """Resets the pixel colors on the canvas."""
        for i in range(len(self.grid)):
            self.grid[i]["color"] = self.canvas_color

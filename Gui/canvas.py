from .depends import *
from Utils.colors import COLORS

class Canvas:
    """Representation of a Pixel Art Canvas."""
    def __init__(self, screen, x, y, width, height, pixel_size):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas_color = COLORS["red1"]
        self.drawing_color = COLORS["black"]
        self.pixel_size = pixel_size
        self.show_grid = False
        # Initializing the grid
        self.grid = []
        for x in range(self.width):
            for y in range(self.height):
                pixel = pygame.Rect(x*self.pixel_size+self.x, y*self.pixel_size+self.y, self.pixel_size, self.pixel_size)
                pixel.center = (pixel.x, pixel.y)
                self.grid.append({"pixel":pixel, "color":self.canvas_color})

    def draw(self):
        """Draws the Canvas to the screen every frame."""
        for pixel in self.grid:
            if self.show_grid == False:
                pygame.draw.rect(self.screen, pixel["color"], pixel["pixel"])
            elif self.show_grid == True:
                pygame.draw.rect(self.screen, pixel["color"], pixel["pixel"], width=1)
            
        
        
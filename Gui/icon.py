from Gui.depends import *

class Icon:
    """Represents an icon image."""
    def __init__(self, filename: str, width: int, height: int):
        self.filename = filename
        self.width = width  
        self.height = height
        self.image = pygame.image.load(filename) # image of the icon
        # scaling the image to the given dimensions
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))


    def draw(self, screen: pygame.Surface, x: int, y: int):
        """Draws the Icon to a given screen and position every frame."""
        screen.blit(self.image, (x, y))
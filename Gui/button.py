from .depends import *
from .label import TextNode
from Utils.colors import COLORS
from Utils.utils import get_darker_color

class Button:
    """A clickable object that performs an operation when clicked."""
    def __init__(self, x, y, width, height, color, text: typing.Optional[TextNode] = None, border_width=0, border_radius=0, border_color=COLORS["black"]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.original_color = self.color
        self.darker_color = get_darker_color(self.color, 11)
        self.text = text
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

    def draw(self, screen):
        """Draws the button to the screen every frame."""
        if self.border_width > 0: # wether we can even see the border
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)
            pygame.draw.rect(screen, (0,0,0), self.rect, width=1, border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        if self.text != None:
            self.text.draw(pos=self.rect.center)


    def onhover(self, mpos):
        """Does something when mouse is hovering over button."""
        if self.rect.collidepoint(mpos):
            self.color = self.darker_color
        else:
            self.color = self.original_color
    
    def clicked(self, mpos):
        """Checks wether the mouse has clicked on this button."""
        if self.rect.collidepoint(mpos):
            return True
        return False
        
            
        
        
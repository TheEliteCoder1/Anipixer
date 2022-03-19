from .depends import *
from .label import TextNode
from Utils.colors import COLORS

class ToggleButton:
    """A clickable object that turns on or off when clicked."""
    def __init__(self, screen, x, y, width, height, on_color, off_color, border_width=0, border_radius=0, border_color=COLORS["black"], font_size=20):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_color = on_color
        self.off_color = off_color
        self.is_on = False
        self.text = TextNode(self.screen, "UI/Fonts/opensans_extrabold.ttf", "Off", font_size, (255,255,255), None)
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

    def draw(self):
        """Draws the button to the screen every frame."""
        if self.is_on == False:
            color = self.on_color
        elif self.is_on == True:
            color = self.off_color
        if self.border_width > 0: # wether we can even see the border
            pygame.draw.rect(self.screen, color, self.rect, border_radius=self.border_radius)
            pygame.draw.rect(self.screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)
            pygame.draw.rect(self.screen, (0,0,0), self.rect, width=1, border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.screen, color, self.rect, border_radius=self.border_radius)

        if self.is_on == False:
            self.text.text = "Off" # sets the text of the toggle button depending on the state of `is_on`.
        elif self.is_on == True:
            self.text.text = "On"

        self.text.draw(pos=self.rect.center)

    def toggle(self, mpos):
        """Toggles the Button to be On or Off."""
        if self.rect.collidepoint(mpos):
            if self.is_on == False:
                self.is_on = True
            elif self.is_on == True:
                self.is_on == False


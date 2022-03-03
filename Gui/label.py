from .depends import *
from Utils import utils

class TextNode:
    """Text Object Representation aside functional `draw_text`, without the position
    argument. Drawing method takes positional argument."""
    def __init__(self, screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, background_color=None, bold=False, italic=False, underline=False):
        self.screen = screen
        self.font_file = font_file
        self.text = text
        self.font_size = font_size
        self.color = color
        self.background_color = background_color
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def draw(self, pos):
        utils.draw_text(screen=self.screen, font_file=self.font_file, text=self.text, font_size=self.font_size, color=self.color, backg=self.background_color, bold=self.bold, italic=self.italic, underline=self.underline, pos=pos)

        
class Label:
    """Text Object Representation aside functional `draw_text`."""
    def __init__(self, screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, background_color=None, bold=False, italic=False, underline=False):
        self.screen = screen
        self.font_file = font_file
        self.text = text
        self.font_size = font_size
        self.color = color
        self.pos = pos
        self.background_color = background_color
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def draw(self):
        """Draws Text To the Screen based on Attrs."""
        utils.draw_text(self.screen, self.font_file, self.text, self.font_size, self.color, self.pos, self.background_color, self.bold, self.italic, self.underline)
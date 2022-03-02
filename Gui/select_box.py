from .depends import *
from .label import TextNode, Label
from Utils.colors import COLORS
from Utils.utils import draw_text, get_text_rect


class SelectBox:
    """Select from data associated with a List."""
    def __init__(self, screen: pygame.Surface, data: list, font: str, text_color: tuple, text_background:typing.Optional[tuple] = None, label_text: typing.Optional[TextNode] = None):
        self.screen = screen
        self.data = data
        self.font = font
        self.text_color = text_color
        self.text_background = text_background
        self.text_rectangles = []
        self.selected_rect = None
        self.selected_option = None
        self.hovering_rect = None
        self.text_idx = 0
        self.selection_color = COLORS["bisque4"]
        self.draw_scale = 18
        self.width_factor = 0.8
        self.height_factor = 2.1
        self.label_text = label_text
        
    def draw(self, x: int, y: int, color: tuple, border_radius=None, outline=False, outline_width=1,
            outline_color=(0,0,0)):
        """Draws the SelectBox to the screen."""
        self.box_rect = pygame.Rect(x, y-self.draw_scale, len(self.data)*self.draw_scale*self.width_factor, len(self.data)*self.draw_scale*self.height_factor)
        self.font_size = self.draw_scale + 5
        if border_radius:
            border_radius = border_radius
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws rectangle
            pygame.draw.rect(self.screen, outline_color, self.box_rect, outline_width, border_radius) # draws outline
        elif outline == False:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws only rectangle

        # Loading UI text rectangles:
        self.ui_text_rectangles = []
        for rect in self.text_rectangles:
            r = pygame.Rect(self.box_rect.x, rect.y, self.box_rect.width, rect.height)
            self.ui_text_rectangles.append(r)

        # Checking for selected rectangle:
        if self.selected_rect != None:
            text_rect = pygame.Rect(self.box_rect.x, self.selected_rect.y, self.box_rect.width, self.selected_rect.height)
            pygame.draw.rect(self.screen, self.selection_color, text_rect)

        # Checking for hovering rectangle
        if self.hovering_rect != None:
            text_rect = pygame.Rect(self.box_rect.x, self.hovering_rect.y, self.box_rect.width, self.hovering_rect.height)
            pygame.draw.rect(self.screen, self.selection_color, text_rect, width=outline_width)
            

        # Drawing Text Elements
        for i, element in enumerate(self.data):
            text_x = self.box_rect.x + self.box_rect.width / 2
            text_y = self.box_rect.y + self.draw_scale * (2*i) if i != 0 else self.box_rect.y + self.draw_scale + outline_width
            if i > 0:
                text_y = text_y + self.draw_scale + outline_width
            draw_text(self.screen, self.font, element, self.font_size, self.text_color, (text_x, text_y), self.text_background)
            self.text_rectangles.append(get_text_rect(self.font, element, self.font_size, (text_x, text_y)))

        # Drawing select box label text
        if self.label_text != None:
            draw_text(screen=self.screen, font_file=self.label_text.font_file, text=self.label_text.text, font_size=self.label_text.font_size, color=self.label_text.color, backg=self.label_text.background_color, bold=self.label_text.bold, italic=self.label_text.italic, underline=self.label_text.underline, pos=(self.box_rect.midtop[0], self.box_rect.midtop[1]-self.height_factor*2))

    def hover_by_iteration(self, direction):
        """Hovering with keyboard presses and directions."""
        if len(self.text_rectangles) > 1: # the conatiner is iterable
            if direction == "down":
                self.text_idx += 1
            elif direction == "up":
                self.text_idx -= 1
        self.hovering_rect = self.ui_text_rectangles[self.text_idx]

    def hover_rect(self, mpos):
        """Draws the hover rectangle if mouse is over an option."""
        for rect in self.text_rectangles:
            if rect.collidepoint(mpos):
                self.hovering_rect = rect

    def is_hovering_box(self, mpos):
        """Checks wether the mouse is hovering over the SelectBox."""
        if hasattr(self, "box_rect"): # Checks wether the draw method has been called yet.
            if self.box_rect.collidepoint(mpos):
                return True
            return False

    def select_hover_rect(self):
        """Selects the Current Hovering rect."""
        if self.hovering_rect != None:
            self.selected_rect = self.hovering_rect
    
    def select_rect(self, mpos):
        """Selects an option."""
        for rect in self.text_rectangles:
            if rect.collidepoint(mpos):
                self.selected_rect = rect

        
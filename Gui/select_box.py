from .depends import *
from .label import TextNode, Label
from Utils.colors import COLORS
from Utils.utils import draw_text, get_text_rect


class SelectBox:
    """Select from data associated with a List."""
    def __init__(self, screen: pygame.Surface, data: list, font: str, text_color: tuple, text_background:typing.Optional[tuple] = None, label_text: typing.Optional[TextNode] = None, selection_color=COLORS["bisque4"]):
        self.screen = screen
        self.data = data
        self.font = font
        self.text_color = text_color
        self.text_background = text_background
        self.selected_rect = None
        self.hovering_rect = None
        self.selection_color = selection_color
        self.draw_scale = 18
        self.width_factor = 0.8
        self.height_factor = 2.1
        self.label_text = label_text
        
    def draw(self, x: int, y: int, color: tuple, border_radius=None, outline=False, outline_width=1,
            outline_color=(0,0,0)):
        """Draws the SelectBox to the screen every frame."""
        # These collections must be instatized here, so we dont add to the original one every frame!
        # UPDATE: Silly mistake caused Extremly low performance. 
        # The length of the list was increasing every second e.g, -> 8, 1000, 1000000, exponentially!
        # Now the size stays at the initial e.g, -> (8) every second that the program runs!
        # New lists must be created every frame so we dont add the same item again and again.
        self.text_rectangles = []
        self.options = [] # list of dictionaries -> {option : ..., position_on_box: ...}
                
        self.box_rect = pygame.Rect(x, y-self.draw_scale, len(self.data)*self.draw_scale*self.width_factor, len(self.data)*self.draw_scale*self.height_factor)
        self.font_size = self.draw_scale + 5
        if border_radius:
            border_radius = border_radius
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws rectangle
            pygame.draw.rect(self.screen, outline_color, self.box_rect, outline_width, border_radius) # draws outline
        elif outline == False:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws only rectangle

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
            txt_rect = get_text_rect(self.font, element, self.font_size, (text_x, text_y))
            self.text_rectangles.append(txt_rect)
            self.options.append({"value":element, "pos":(txt_rect.x, txt_rect.y)})

        # Loading UI text rectangles:
        self.ui_text_rectangles = []
        for rect in self.text_rectangles:
            r = pygame.Rect(self.box_rect.x, rect.y, self.box_rect.width, rect.height+self.height_factor)
            self.ui_text_rectangles.append(r)
            
        # Drawing select box label text
        if self.label_text != None:
            self.label_text.draw(pos=(self.box_rect.midtop[0], self.box_rect.midtop[1]-self.height_factor*2))
            
    def hover_rect(self, mpos):
        """Draws the hover rectangle if mouse is over an option."""
        if hasattr(self, "text_rectangles"):
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

    def get_selected_value(self) -> str:
        """Gets the selected value, if there is one."""
        if self.selected_rect != None:
            for i in range(len(self.options)):
                if self.options[i]["pos"] == (self.selected_rect.x, self.selected_rect.y):
                    return self.options[i]["value"]
    
    def select_rect(self, mpos):
        """Selects an option."""
        if hasattr(self, "text_rectangles"):
            for rect in self.text_rectangles:
                if rect.collidepoint(mpos):
                    self.selected_rect = rect

        
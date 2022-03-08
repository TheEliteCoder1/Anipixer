from .depends import *
from Utils.colors import COLORS


class ColorPallete:
    """A Pallete of colors."""
    def __init__(self, screen, x, y, color_values: typing.List[tuple], color_button_size: tuple):
        self.screen = screen
        self.x = x
        self.y = y
        self.color_values = color_values
        self.color_button_size = color_button_size
        self.selected_color = None
        self.draw_scale = 18
        self.width_factor = 2.5
        self.height_factor = 0.5

    def draw(self, outline=True, color=(255,255,255), border_color=(0,0,0), border_width=1, border_radius=1):
        """Draws the ColorPallete to the screen every frame."""
        # Drawing Color Pallete Body
        width = len(self.color_values)*self.draw_scale*self.width_factor
        height = len(self.color_values)*self.draw_scale*self.height_factor
        self.box_rect = pygame.Rect(self.x, self.y-self.draw_scale, width, height)
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)
            # Drawing Outline
            pygame.draw.rect(self.screen, border_color, self.box_rect, width=border_width, border_radius=border_radius)
        else:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)

        self.swatches = [] # list of color swatches.
        for i in range(len(self.color_values)):
            if i == 0:
                swatch_x = self.box_rect.x + self.draw_scale + border_width
                swatch_y = self.box_rect.y + self.draw_scale + border_width
                first_x_y = (swatch_x, swatch_y)
            if i > 0:
                swatch_x = first_x_y[0]*(i+1)
                swatch_y = first_x_y[1]
            if i == len(self.color_values):
                swatch_x = first_x_y[0]*(i)
                swatch_y = first_x_y[1]
            data = {"color":self.color_values[i], "rect":pygame.Rect(swatch_x, swatch_y, *self.color_button_size)}
            self.swatches.append(data)
        for i in range(len(self.swatches)):
            pygame.draw.rect(self.screen, self.swatches[i]["color"], self.swatches[i]["rect"], border_radius=3)
            pygame.draw.rect(self.screen, COLORS["black"], self.swatches[i]["rect"], width=1, border_radius=3)

    def get_selected_color(self, mpos):
        """Finds the selected color of the ColorPallete."""
        for i in range(len(self.swatches)):
            if self.swatches[i]["rect"].collidepoint(mpos):
                self.selected_color = self.swatches[i]["color"]
        
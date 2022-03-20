from .depends import *
from .icon import Icon
from .label import TextStyle, TextNode
from Utils.utils import get_text_rect, draw_text

class ToolBar:
    """A Bar of tools represented by icons that can be clicked."""
    def __init__(self, screen, x: int, y: int, tool_names: list, tool_images: list, icon_size: tuple):
        self.screen = screen
        self.x = x
        self.y = y
        self.tool_names = tool_names # list of tool names
        self.tool_images = tool_images # list of tool images
        self.icon_size = icon_size # size of all icons
        self.selected_tool = None
        self.draw_scale = 18
        self.width_factor = 1.5
        self.base_width = 3
        self.icon_label_spacing = 15
        self.height_factor = 3
        self.space_factor = self.icon_size[1]*1.5
        
    def draw(self, outline=True, color=(255,255,255), border_color=(0,0,0), border_width=1, border_radius=1, 
    show_labels_beside_icons=False,
    text_style=TextStyle("UI/Fonts/proxima_nova.ttf", 13, (0,0,0), None)
    ):
        """
        Draws the ToolBar to the screen every frame.
        If the `show_labels_beside_icons` argument is false, only icons will show.
        Otherwise, if the argument is true, icons will be display beside the name of the tools using labels.
        """
        # Drawing ToolBar Body
        width = self.base_width*self.draw_scale*self.width_factor
        height = len(self.tool_names)*self.draw_scale*self.height_factor
        self.box_rect = pygame.Rect(self.x, self.y, width, height)
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)
            # Drawing Outline
            pygame.draw.rect(self.screen, border_color, self.box_rect, width=border_width, border_radius=border_radius)
        else:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)

        # Collecting Tool Data
        self.tools = []
        for i in range(len(self.tool_names)):
            tool_x = self.x + ((width/2) - (border_width*2) - (self.width_factor*2))
            tool_y = self.y + self.height_factor
            if i == 1:
                tool_y = tool_y + self.space_factor
            if i > 1:
                tool_y = tool_y + (self.space_factor*i)
            data = {"name":self.tool_names[i], "pos":(tool_x, tool_y), "image":self.tool_images[i], "rect":pygame.Rect(self.x, tool_y, width, height / len(self.tool_names))}
            self.tools.append(data)

        # Drawing Tools
        if show_labels_beside_icons == False:
            for i in range(len(self.tools)):
                # creating an icon from tool data and drawing it
                icon_image = Icon(self.tools[i]["image"], *self.icon_size)
                icon_image.draw(self.screen, *self.tools[i]["pos"])
        else:
            for i in range(len(self.tools)):
                # creating a text node object from a given text_style, and drawing it alongside it's icon.
                icon_name = TextNode(self.screen, text_style.font_file, self.tools[i]["name"], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                pos = (self.tools[i]["rect"].x+(self.icon_label_spacing*1.9), self.tools[i]["rect"].center[1]-5)
                icon_name_txt_rect = get_text_rect(icon_name.font_file, icon_name.text, icon_name.font_size, pos)
                icon_image = Icon(self.tools[i]["image"], *self.icon_size)
                icon_name.draw(pos) # draw the text node at the center.
                icon_image.draw(self.screen, *(icon_name_txt_rect.width + (self.icon_label_spacing*1.9), self.tools[i]["rect"][1])) # draw to the right of the text node.


    def get_selected_tool(self, mpos):
        """Gets the selected tool based on the position of the mouse click."""
        for i in range(len(self.tools)):
            if self.tools[i]["rect"].collidepoint(mpos):
                self.selected_tool = self.tools[i]["name"]

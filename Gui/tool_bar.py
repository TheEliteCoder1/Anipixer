from Gui.depends import *
from .icon import Icon

class ToolBar:
    """A Bar of tools with icons that can be clicked"""
    def __init__(self, screen, x: int, y: int, tool_names: list, tool_images: list, icon_size: tuple):
        self.screen = screen
        self.x = x
        self.y = y
        self.tool_names = tool_names # list of tool names
        self.tool_images = tool_images # list of tool images
        self.icon_size = icon_size # size of all icons
        self.selected_tool = None
        self.draw_scale = 18
        self.width_factor = 2
        self.height_factor = 3
        self.space_factor = self.icon_size[1]*1.5
        
    def draw(self, outline=True, color=(255,255,255), border_color=(0,0,0), border_width=1, border_radius=1):
        """Draws the ToolBar to the screen every frame."""
        # Drawing ToolBar Body
        width = len(self.tool_names)*self.draw_scale*self.width_factor
        height = len(self.tool_names)*self.draw_scale*self.height_factor
        self.box_rect = pygame.Rect(self.x, self.y, width, height)
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)
            # Drawing Outline
            pygame.draw.rect(self.screen, border_color, self.box_rect, width=border_width, border_radius=border_radius)
        else:
            pygame.draw.rect(self.screen, color, self.box_rect, border_radius=border_radius)

        self.tools = [] # list of tools.
        for i in range(len(self.tool_names)):
            tool_x = self.x + ((width/2) - (border_width*2) - (self.width_factor*2))
            tool_y = self.y + self.height_factor
            if i > 0:
                tool_y = tool_y + self.space_factor
            data = {"name":self.tool_names[i], "pos":(tool_x, tool_y), "image":self.tool_images[i], "rect":pygame.Rect(self.x, tool_y, width, height / len(self.tool_names))}
            self.tools.append(data)
        # Drawing Tools
        for i in range(len(self.tools)):
            # creating an icon from tool data and drawing it
            icon_image = Icon(self.tools[i]["image"], *self.icon_size)
            icon_image.draw(self.screen, *self.tools[i]["pos"])


    def get_selected_tool(self, mpos):
        """Gets the selected tool based on the position of the mouse click."""
        for i in range(len(self.tools)):
            if self.tools[i]["rect"].collidepoint(mpos):
                self.selected_tool = self.tools[i]["name"]

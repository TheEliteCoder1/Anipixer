from Gui.depends import *

class MenuBar:
    def __init__(self, screen: pygame.Surface, menu_list: list, bar_height: int):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.bar_width = screen.get_width()
        self.bar_height = bar_height

    


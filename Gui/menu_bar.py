from .depends import *
from .label import TextStyle, TextNode
from Utils.utils import get_text_rect
from Utils.colors import COLORS

class MenuBar:
    def __init__(self, screen: pygame.Surface, menu_names_list: list, menu_options_dict: dict, bar_height: int, hover_color=(0,0,0), menu_hover_color=(255,255,255)):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.bar_width = screen.get_width()
        self.menu_names_list = menu_names_list
        self.menu_options_dict = menu_options_dict
        self.hovering_menu_title = None
        self.hovering_option = None
        self.options = None
        self.bar_height = bar_height
        self.hover_color = hover_color
        self.max_option_text_rect = 72
        self.menu_hover_color = menu_hover_color
        self.menu_space_factor = 10

    def draw(self, mpos, bar_color=COLORS['azure4'], text_style=TextStyle("UI/Fonts/fira.ttf", 20, (0,0,0), None)):
        # drawing the body of the menu bar.
        self.bar_rect = pygame.Rect(self.x, self.y, self.bar_width, self.bar_height)
        pygame.draw.rect(self.screen, bar_color, self.bar_rect)

        # drawing the menu titles.
        self.menu_titles = []
        for i in range(len(self.menu_names_list)):
            if i == 0:
                menu_title_x = self.bar_rect.x + 30
                menu_title_y = self.bar_rect.y/2+12
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
                first_x_y = (menu_title_x, menu_title_y)
            elif i > 0:
                menu_title_x = (first_x_y[0]*(i+1))+menu_title_rect.width + self.menu_space_factor
                menu_title_y = first_x_y[1]
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
            elif i == len(self.menu_names_list):
                menu_title_x = (first_x_y[0]*i)+menu_title_rect.width + self.menu_space_factor
                menu_title_y = first_x_y[1]
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
            self.menu_titles.append({"pos":(menu_title_x, menu_title_y), "title":menu_title, "rect":menu_title_rect, "options":menu_options, "index":i})

        # checking for the hovered menu titles.
        if self.hovering_menu_title != None and self.is_hovering(mpos) == True:
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["title"].text == self.hovering_menu_title.text:
                    self.menu_titles[i]["title"].color = self.hover_color
                    pygame.draw.rect(self.screen, self.menu_hover_color, self.menu_titles[i]["rect"])

        for i in range(len(self.menu_titles)):
            self.menu_titles[i]["title"].draw(self.menu_titles[i]["pos"])

        # draw the options of the menu that was clicked.
        if self.options != None and self.is_hovering(mpos) == True:
            self.options_list = [] # list with all gui elements of options.
            options = self.menu_options_dict[self.menu_titles[self.options["index"]]["title"].text]
            for i in range(len(options)):
                if i == 0:
                    option_x = self.menu_titles[self.options["index"]]["rect"].x
                    option_y = self.menu_titles[self.options["index"]]["rect"].y+self.bar_height
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                    option_text_rect = pygame.Rect(option_x, option_y, self.max_option_text_rect, self.menu_titles[self.options["index"]]["rect"].height)
                    first_x_y = (option_x, option_y)
                elif i > 0:
                    option_x = first_x_y[0]
                    option_y = first_x_y[1]*(i+1)
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                    option_text_rect = pygame.Rect(option_x, option_y, self.max_option_text_rect, self.menu_titles[self.options["index"]]["rect"].height)
                elif i == len(options):
                    option_x = first_x_y[0]
                    option_y = first_x_y[1]*(i)
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color, text_style.bold, text_style.italic, text_style.underline)
                    option_text_rect = pygame.Rect(option_x, option_y, self.max_option_text_rect, self.menu_titles[self.options["index"]]["rect"].height)
                self.options_list.append({"pos":(option_x, option_y), "text":option_text, "rect":option_text_rect})


        if hasattr(self, "options_list"):
            for i in range(len(self.options_list)):
                if self.hovering_option != None and self.options_list[i]["text"].text == self.hovering_option:
                    self.options_list[i]["text"].color = self.hover_color
                    pygame.draw.rect(self.screen, self.menu_hover_color, self.options_list[i]["rect"])
                else:
                    pygame.draw.rect(self.screen, bar_color, self.options_list[i]["rect"])
                pygame.draw.rect(self.screen, (0,0,0), self.options_list[i]["rect"], 1)
                self.options_list[i]["text"].draw(self.options_list[i]["rect"].center)


    def onhover(self, mpos):
        """Performs an action if the mouse is hovering over one of the menus in the menu bar."""
        if hasattr(self, "menu_titles") and hasattr(self, "bar_rect") and hasattr(self, "options_list"):
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["rect"].collidepoint(mpos) and self.bar_rect.collidepoint(mpos):
                    self.hovering_menu_title = self.menu_titles[i]["title"]
            for i in range(len(self.options_list)):
                if self.options_list[i]["rect"].collidepoint(mpos):
                    self.hovering_option = self.options_list[i]["text"].text

    def is_hovering(self, mpos):
        if hasattr(self, "bar_rect"):
            if self.bar_rect.collidepoint(mpos):
                return True
            else:
                return False 

    def open_menu(self, mpos):
        """If any of the menus in the menu bar were clicked, we will display the options below."""
        if hasattr(self, "menu_titles"):
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["rect"].collidepoint(mpos):
                    self.options = {"options":self.menu_titles[i]["options"], "index":i}



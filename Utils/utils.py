from Gui.depends import *

def draw_text(screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, backg=None, bold=False, italic=False, underline=False):
    """Draws text to the screen given a font file and text."""
    font = pygame.font.Font(font_file, font_size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    if backg == None:
        t = font.render(text, 1, color)
    t = font.render(text, 1, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def get_text_rect(font_file, text, font_size, pos):
    """Returns the bounding rectangle of a text object drawn to the screen."""
    font = pygame.font.Font(font_file, font_size)
    t = font.render(text, 1, (0,0,0))
    textRect = t.get_rect()
    textRect.center = pos
    return textRect

def get_screen_parts(screen: pygame.Surface) -> dict:
    """Get usefull parts of the screen as variables returned in a dict where key is the variable name alongside it's value."""
    center_screen_x = screen.get_width() // 2
    center_screen_y = screen.get_height() // 2
    margin_top = 50 
    margin_left = 20
    center_screen_pos = (center_screen_x, center_screen_y)  
    top_middle_screen = (center_screen_x, margin_top)
    constants_dict = {
        "center_screen_x":center_screen_x, 
        "center_screen_y":center_screen_y, 
        "center_screen_pos":center_screen_pos,
        "top_middle_screen":top_middle_screen,
        "margin_top":margin_top,
        "margin_left":margin_left
    }
    return constants_dict

def set_custom_cursor(screen: pygame.Surface, cursor, cursor_pos: tuple):
    """Sets the cursor of the application."""
    screen.blit(cursor, cursor_pos)
    
    
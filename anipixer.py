from Gui.depends import *
from Gui.button import Button
from Gui.label import TextNode
from Utils.utils import *
import paintlib
from paintlib import basic_colors_list
from paintlib import WHITE, BLACK

"""Runtime Variables"""
sw, sh = 500, 400
screen = pygame.display.set_mode((sw, sh))
screen_parts = get_screen_parts(screen)
refresh_rate = 120
cursor_size = (35, 35)
cursor = pygame.transform.smoothscale(pygame.image.load(paintlib.CURSORS["pointer"]), cursor_size)
cursor_rect = cursor.get_rect()
app_background_color = WHITE
clock = pygame.time.Clock()

"""Setting Up User Interface."""
clear_btn_x, clear_btn_y = screen.get_width() - 200, screen_parts["margin_top"]
clear_btn_txt = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Clear", 20, BLACK)
clear_btn = Button(clear_btn_x, clear_btn_y, 90, 50, WHITE, text=clear_btn_txt, border_width=7, border_radius=15, border_color=BLACK)
buttons = [clear_btn]

"""Drawing Interface to Screen."""
def draw_app(screen):
    screen.fill(app_background_color) # setting the background color
    for button in buttons: # drawing all buttons
        button.draw(screen)
        

"""Running Application."""
while True:
    running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    draw_app(screen)
    pygame.display.update()

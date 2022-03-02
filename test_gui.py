"""Test /GUI code here."""
from Gui.depends import *
from Gui.label import TextNode
from Gui.select_box import SelectBox
from Utils.utils import *
import paintlib
from paintlib import colors_dict

"""Testing GUI Runtime Parameters"""
sw, sh = 500, 500
screen = pygame.display.set_mode((sw, sh))
screen_parts = get_screen_parts(screen)
refresh_rate = 120
cursor_size = (40, 40)
cursor = pygame.transform.smoothscale(pygame.image.load(paintlib.CURSORS["pointer"]), cursor_size)
cursor_rect = cursor.get_rect()
clock = pygame.time.Clock()

"""Instantize Test Classes Here"""
tx = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Basic Colors", 25, paintlib.WHITE, paintlib.BLACK)
sb = SelectBox(screen, colors_dict["basic_colors"], paintlib.FONTS["ui_font"], colors_dict['a']['azure1'], label_text=tx)
def select_box_test(screen):
    screen.fill(paintlib.WHITE)
    sb.draw(*(25, screen.get_height()//2-50), colors_dict['b']['brown1'], border_radius=30, outline=True, outline_width=7,
            outline_color=colors_dict['b']['black'])

def draw_cursor(screen, cursor, cursor_rect):
    cursor_rect.center = pygame.mouse.get_pos()  # update position 
    screen.blit(cursor, cursor_rect) 

def run_test(test_func: typing.Callable):
    """Runs any test, by updating and displaying it on the runtime parameters."""
    running = True
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(refresh_rate)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for mouse click
                mpos = pygame.mouse.get_pos()
                sb.select_rect(mpos)

            if event.type == pygame.MOUSEMOTION:
                # Check if mouse is moving
                mpos = pygame.mouse.get_pos()
                sb.hover_rect(mpos)

            if event.type == pygame.KEYDOWN:
                # Checking for key presses
                mpos = pygame.mouse.get_pos()
                if sb.is_hovering_box(mpos):
                    keys=pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        sb.hover_by_iteration("up")
                    elif keys[pygame.K_DOWN]:
                        sb.hover_by_iteration("down")
                    elif keys[pygame.K_RETURN]:
                        sb.select_hover_rect()


        test_func(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

# Run Your Tests Here
run_test(select_box_test)

            

    
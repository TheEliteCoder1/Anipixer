"""Test /GUI code here."""
import random
from Gui.depends import *
from Gui.label import TextNode
from Gui.select_box import SelectBox
from Gui.button import Button
from Gui.color_pallete import ColorPallete
from Gui.canvas import Canvas
from Gui.icon import Icon
from Gui.tool_bar import ToolBar
from Utils.utils import *
from Utils.colors import get_colors_list
import paintlib
from paintlib import colors_dict, CURSORS

"""Testing GUI Runtime Parameters"""
sw, sh = 500, 500
screen = pygame.display.set_mode((sw, sh))
screen_parts = get_screen_parts(screen)
refresh_rate = 120
cursor_size = (35, 35)
cursor = pygame.transform.smoothscale(pygame.image.load(paintlib.CURSORS["pointer"]), cursor_size)
cursor_rect = cursor.get_rect()
clock = pygame.time.Clock()

"""Instantize Test Classes Here"""
txt = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Basic Colors", 25, paintlib.WHITE, paintlib.BLACK)
sb = SelectBox(screen, colors_dict["basic_colors"], paintlib.FONTS["ui_font"], colors_dict['a']['azure1'], label_text=txt, selection_color=paintlib.BLACK)
btn_txt = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Clear", font_size=50, color=paintlib.BLACK)
btn = Button(300, 250, 150, 70, paintlib.WHITE, text=btn_txt, border_width=7, border_radius=15, border_color=colors_dict["b"]["black"])
cp = ColorPallete(screen, 50, 50, color_values=paintlib.basic_colors_list, color_button_size=(30, 30))
cv = Canvas(screen, *screen_parts["canvas_pos"], 13, 12, 25, grid=[])
tool_names = ["Cursor", "Eraser"]
tool_images = [CURSORS["pointer"], CURSORS["eraser"]] # Note: Order must correspond with name order.
tb = ToolBar(screen, 50, 50, tool_names, tool_images, icon_size=cursor_size)

def draw_tool_bar(screen):
    screen.fill(paintlib.WHITE)
    tb.draw(outline=True, color=paintlib.WHITE, border_color=colors_dict['c']['crimson'], border_width=5, border_radius=5)

def draw_canvas(screen):
    """Canvas draw method."""
    screen.fill(paintlib.WHITE)
    cv.draw(cv.grid, cv.canvas_boundary, show_grid=False, select_mode=False)

def draw_select_box(screen, bg_color):
    """SelectBox draw method."""
    screen.fill(bg_color)
    sb.draw(*(25, screen.get_height()//2-50), colors_dict['b']['brown1'], border_radius=30, outline=True, outline_width=7,
            outline_color=colors_dict['b']['black'])

def draw_color_pallete(screen):
    """ColorPallete draw method."""
    screen.fill(paintlib.WHITE)
    cp.draw(outline=True, color=paintlib.WHITE, border_color=paintlib.BLACK, border_width=3, border_radius=5)
    # outline=True, color=COLORS["white"], border_color=COLORS["black"], border_width=1, border_radius=1)
    
def draw_button(screen):
    """Button draw method"""
    screen.fill(paintlib.WHITE)
    btn.draw(screen)

def tool_bar_test():
    """Sample ToolBar Test"""
    running = True
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(refresh_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                pass

        draw_tool_bar(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

def canvas_test():
    """Sample Canvas Test"""
    running = True
    is_mouse_dragging = False
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(refresh_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    cv.show_grid = False
                elif event.key == pygame.K_g:
                    cv.show_grid = True
                elif event.key == pygame.K_1:
                    cv.drawing_color = colors_dict['r']["red1"]
                    cv.erase_mode = False
                elif event.key == pygame.K_2:
                    cv.drawing_color = colors_dict['b']["blue"]
                    cv.erase_mode = False
                elif event.key == pygame.K_3:
                    cv.drawing_color = colors_dict['g']["green"]
                    cv.erase_mode = False
                elif event.key == pygame.K_e:
                    cv.erase_mode = True
                elif event.key == pygame.K_c:
                    cv.clear_canvas()
                elif event.key == pygame.K_l:
                    cv.line_tool(mpos)
                
            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_dragging = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_dragging = True

        if is_mouse_dragging == True:
            mpos = pygame.mouse.get_pos()
            cv.paint_pixel(mpos)

        draw_canvas(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

def color_pallete_test():
    """Sample ColorPallete Test"""
    running = True
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(refresh_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        draw_color_pallete(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()
    
def button_test():
    """Sample Button Test."""
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
                # check if clicked
                mpos = pygame.mouse.get_pos()
                if btn.clicked(mpos):
                    print(f"{btn.text.text} was clicked.")

            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                btn.onhover(mpos)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    btn.rect.y -= 10
                    btn.color = random.choice(get_colors_list())
                    btn.text.color = random.choice(get_colors_list())
                elif keys[pygame.K_s]:
                    btn.rect.y += 10
                    btn.color = random.choice(get_colors_list())
                    btn.text.color = random.choice(get_colors_list())
                elif keys[pygame.K_a]:
                    btn.rect.x -= 10
                    btn.color = random.choice(get_colors_list())
                    btn.text.color = random.choice(get_colors_list())
                elif keys[pygame.K_d]:
                    btn.rect.x += 10
                    btn.color = random.choice(get_colors_list())
                    btn.text_color = random.choice(get_colors_list())


        draw_button(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

def select_box_test():
    """Sample SelectBox Test."""
    running = True
    background_color = colors_dict["g"]["gray50"]
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(refresh_rate)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Change background color of window based on selected option.
                mpos = pygame.mouse.get_pos()
                sb.select_rect(mpos)
                if sb.get_selected_value() != None:
                    background_color = colors_dict["basic_colors"][sb.get_selected_value()]

            if event.type == pygame.MOUSEMOTION:
                # Check if mouse is hover over SelectBox.
                mpos = pygame.mouse.get_pos()
                sb.hover_rect(mpos)

        draw_select_box(screen, background_color)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

"""Run Your Tests Here (CLI)."""
if len(sys.argv) >= 2: # test_gui.py [test_name]
    test = sys.argv[1]
    # runs the function by calling the function name from string to evaluated literal function.
    eval(test)()
else:
    print("Please type in the name of the test.")
            

    
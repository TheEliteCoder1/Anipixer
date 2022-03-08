from Gui.depends import *
from Gui.button import Button
from Gui.label import TextNode
from Gui.color_pallete import ColorPallete
from Gui.canvas import Canvas
from Utils.utils import *
import paintlib
from paintlib import basic_colors_list
from paintlib import WHITE, BLACK

"""Runtime Variables"""
sw, sh = 700, 600
screen = pygame.display.set_mode((sw, sh))
screen_parts = get_screen_parts(screen)
refresh_rate = 120
cursor_size = (35, 35)
cursor = pygame.transform.smoothscale(pygame.image.load(paintlib.CURSORS["pointer"]), cursor_size)
cursor_rect = cursor.get_rect()
app_background_color = WHITE
clock = pygame.time.Clock()

"""Setting Up User Interface."""
color_pallete = ColorPallete(screen, 20, 30, color_values=paintlib.basic_colors_list, color_button_size=(30, 30))
clear_btn_x, clear_btn_y = screen_parts["screen_width"] - 300,  color_pallete.y/2+10
clear_btn_txt = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Clear", 20, BLACK)
clear_btn = Button(clear_btn_x, clear_btn_y, 90, 50, WHITE, text=clear_btn_txt, border_width=7, border_radius=15, border_color=BLACK)
erase_btn_x, erase_btn_y = screen_parts["screen_width"] - 200,  color_pallete.y/2+10
erase_btn_txt = TextNode(screen, paintlib.FONTS["ui_thick_font"], "Erase", 20, BLACK)
erase_btn = Button(erase_btn_x, erase_btn_y, 90, 50, WHITE, text=erase_btn_txt, border_width=7, border_radius=15, border_color=BLACK)
canvas = Canvas(screen, *screen_parts["canvas_pos"], 15, 19, 25)
buttons = [clear_btn, erase_btn]

"""Drawing Interface to Screen."""
def draw_app(screen):
    screen.fill(app_background_color) # setting the background color
    for button in buttons: # drawing all buttons
        button.draw(screen)
    # Drawing color pallete
    color_pallete.draw(outline=True, color=paintlib.WHITE, border_color=paintlib.BLACK, border_width=3, border_radius=5)
    canvas.draw()

"""Running Application."""
def program():
    running = True
    is_mouse_dragging = False
    pygame.mouse.set_visible(False)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    canvas.show_grid = False
                elif event.key == pygame.K_g:
                    canvas.show_grid = True
            #     elif event.key == pygame.K_1:
            #         canvas.drawing_color = paintlib.RED
            #         canvas.erase_mode = False
            #     elif event.key == pygame.K_2:
            #         canvas.drawing_color = paintlib.BLUE
            #         canvas.erase_mode = False
            #     elif event.key == pygame.K_3:
            #         canvas.drawing_color = paintlib.GREEN
            #         canvas.erase_mode = False
            #     elif event.key == pygame.K_e:
            #         canvas.erase_mode = True
            #     elif event.key == pygame.K_c:
            #         canvas.clear_canvas()
                
            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_dragging = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_dragging = True
                mpos = pygame.mouse.get_pos()
                """Checking if the Color Pallete was used, and if so set the color."""
                color_pallete.get_selected_color(mpos)
                if color_pallete.selected_color != None:
                    canvas.drawing_color = color_pallete.selected_color
                if clear_btn.clicked(mpos):
                    canvas.clear_canvas()
                if erase_btn.clicked(mpos):
                    color_pallete.selected_color = canvas.canvas_color
                
        if is_mouse_dragging == True: # Mouse draging tools will work here.
            mpos = pygame.mouse.get_pos()
            canvas.paint_pixel(mpos)


        draw_app(screen)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

program()

from Gui.depends import pygame
from Gui.button import Button
from Gui.label import TextNode
from Gui.icon import Icon
from Gui.tool_bar import ToolBar
from Gui.color_pallete import ColorPallete
from Gui.canvas import Canvas
from Utils.utils import *
import paintlib
from paintlib import basic_colors_list
from Utils.filemenu import save_canvas_to_anp, open_canvas_from_anp
from paintlib import WHITE, BLACK, CURSORS, FONTS, colors_dict


"""Drawing Interface to Screen."""
def draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar):
    screen.fill(app_background_color) # setting the background color
    for button in buttons: # drawing all buttons
        button.draw(screen)
    # Drawing color pallete
    color_pallete.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15, swatch_outline=WHITE)
    canvas.draw(canvas.grid, canvas.canvas_boundary)
    tool_bar.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15)


"""Running Application."""
def program():
    """Runtime Variables"""
    sw, sh = 500, 620
    screen = pygame.display.set_mode((sw, sh), HWSURFACE|DOUBLEBUF|RESIZABLE)
    screen_title = "Anipixer"
    pygame.display.set_caption(screen_title)
    screen_parts = get_screen_parts(screen)
    refresh_rate = 120
    cursor_size = (35, 35)
    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["pointer"]), cursor_size)
    cursor_rect = cursor.get_rect()
    app_background_color = WHITE
    clock = pygame.time.Clock()
    running = True
    is_mouse_dragging = False
    pygame.mouse.set_visible(False)
    """Setting Up User Interface."""
    color_pallete = ColorPallete(screen, 20, 30, color_values=basic_colors_list, color_button_size=(30, 30))
    clear_btn_x, clear_btn_y = screen_parts["screen_width"] - 270,  color_pallete.y/2+5
    clear_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Clear", 25, WHITE)
    clear_btn = Button(clear_btn_x, clear_btn_y, 100, 55, color=colors_dict['r']["red3"], text=clear_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    tool_names = ["Cursor", "Eraser"]
    tool_images = [CURSORS["pointer"], CURSORS["eraser"]] # Note: Order must correspond with name order.
    tool_bar = ToolBar(screen, 20, 100, tool_names, tool_images, icon_size=cursor_size)
    tool_bar.selected_tool = "Cursor"
    tool_bar_width = tool_bar.base_width*tool_bar.draw_scale*tool_bar.width_factor
    # note: grid argument can also be empty list
    max_canvas_presets = (int((sw - 200)/25), int((sh - 120)/25), 25)
    canvas = Canvas(screen, *(tool_bar_width*3, screen_parts["canvas_pos"][1]), *max_canvas_presets, grid=[])
    canvas.drawing_color = color_pallete.selected_color
    # scenario: test project loading:
    # open_canvas_from_anp('testFiles/test.anp')
    buttons = [clear_btn]
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # saving grid
                save_canvas_to_anp(canvas, 'testFiles/test2.anp')
                running = False
                pygame.quit()
                quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    canvas.show_grid = False
                elif event.key == pygame.K_g:
                    canvas.show_grid = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_dragging = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_dragging = True
                mpos = pygame.mouse.get_pos()
                # First check tool being used
                tool_bar.get_selected_tool(mpos)
                # always check for color pallete clicks
                color_pallete.get_selected_color(mpos)
                if tool_bar.selected_tool == "Cursor":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["pointer"]), cursor_size) # change apperance for the tool
                    canvas.drawing_color = color_pallete.selected_color # use color from pallete
                elif tool_bar.selected_tool == "Eraser":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["eraser"]), cursor_size)
                    canvas.drawing_color = canvas.canvas_color # use background color attribute of canvas.
                """These Buttons Below Can Be Clicked With Any Tool"""
                if clear_btn.clicked(mpos):
                    canvas.clear_canvas()

            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                
        if is_mouse_dragging == True: # Mouse draging tools will work here.
            mpos = pygame.mouse.get_pos()
            if tool_bar.selected_tool == "Cursor" or tool_bar.selected_tool == "Eraser":
                canvas.paint_pixel(mpos)
    

        draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

program()

from Gui.depends import *
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
    color_pallete.draw(outline=True, color=WHITE, border_color=colors_dict['c']['crimson'], border_width=7, border_radius=15, swatch_outline=BLACK)
    canvas.draw(canvas.grid, canvas.canvas_boundary)
    tool_bar.draw(outline=True, color=WHITE, border_color=colors_dict['c']['crimson'], border_width=7, border_radius=15)


"""Running Application."""
def program():
    """Runtime Variables"""
    sw, sh = 700, 600
    screen = pygame.display.set_mode((sw, sh))
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
    clear_btn = Button(clear_btn_x, clear_btn_y, 100, 55, color=colors_dict['r']["red3"], text=clear_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['banana'])
    # color=colors_dict['d']["dodgerblue3"]
    # border_colors_dict['e']['emeraldgreen']
    # grid argument can also be empty list, if new project. open_canvas_from_anp('test.anp')
    canvas = Canvas(screen, *screen_parts["canvas_pos"], 15, 19, 25, grid=open_canvas_from_anp('test.anp'))
    canvas.drawing_color = color_pallete.selected_color
    tool_names = ["Cursor", "Eraser", "Line"]
    tool_images = [CURSORS["pointer"], CURSORS["eraser"], CURSORS["line"]] # Note: Order must correspond with name order.
    tool_bar = ToolBar(screen, 20, 100, tool_names, tool_images, icon_size=cursor_size)
    tool_bar.selected_tool = "Cursor"
    buttons = [clear_btn]
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # saving grid
                save_canvas_to_anp(canvas, 'test.anp')
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
                if tool_bar.selected_tool == "Cursor":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["pointer"]), cursor_size) # change apperance for the tool
                    color_pallete.get_selected_color(mpos)
                    canvas.drawing_color = color_pallete.selected_color
                elif tool_bar.selected_tool == "Eraser":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["eraser"]), cursor_size)
                    color_pallete.selected_color = canvas.canvas_color
                    canvas.drawing_color = color_pallete.selected_color
                elif tool_bar.selected_tool == "Line":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["line"]), cursor_size)
                """These Buttons Below Can Be Clicked With Any Tool"""
                if clear_btn.clicked(mpos):
                    canvas.clear_canvas()
                    
                
        if is_mouse_dragging == True: # Mouse draging tools will work here.
            mpos = pygame.mouse.get_pos()
            if tool_bar.selected_tool == "Cursor" or tool_bar.selected_tool == "Eraser":
                canvas.paint_pixel(mpos)
            elif tool_bar.selected_tool == "Line":
                canvas.line_tool(mpos)

        draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

program()

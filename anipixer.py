from Gui.button import Button
from Gui.toggle_button import ToggleButton
from Gui.label import TextNode, TextStyle
from Gui.icon import Icon
from Gui.tool_bar import ToolBar
from Gui.color_pallete import ColorPallete
from Gui.canvas import Canvas
from Gui.menu_bar import MenuBar
from Utils.utils import *
from tkinter import Tk
import ntpath
import tkinter.filedialog
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import paintlib
from paintlib import basic_colors_list
from Utils.filemenu import save_canvas_to_anp, open_canvas_from_anp
from paintlib import WHITE, BLACK, CURSORS, FONTS, colors_dict

def path_leaf(path):
    """Gets filename only from full path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

"""Drawing Interface to Screen."""
def draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar, show_grid, menu_bar, mpos, hide_options, screen_title, select_mode):
    screen.fill(app_background_color) # setting the background color
    pygame.display.set_caption(screen_title)
    for button in buttons: # drawing all buttons
        button.draw(screen)
    # Drawing color pallete
    color_pallete.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15, swatch_outline=WHITE)
    canvas.draw(canvas.grid, canvas.canvas_boundary, show_grid, select_mode)
    tool_bar.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15)
    menu_bar.draw(mpos=mpos, bar_color=colors_dict['r']['royalblue1'], text_style=TextStyle("UI/Fonts/fira.ttf", 20, WHITE, None), hide_options=hide_options)


"""Running Application."""
def program():
    """Runtime Variables"""
    sw, sh = 700, 640
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
    color_pallete = ColorPallete(screen, 20, 50, color_values=basic_colors_list, color_button_size=(30, 30))
    color_pallete_width = len(color_pallete.color_values)*color_pallete.draw_scale*color_pallete.width_factor
    clear_btn_x, clear_btn_y = color_pallete_width+35,  color_pallete.y/2+15
    clear_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Clear", 25, WHITE)
    clear_btn = Button(clear_btn_x, clear_btn_y, 100, 55, color=colors_dict['r']["red3"], text=clear_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    grid_toggle_btn = ToggleButton(screen, color_pallete_width+clear_btn.width+45, clear_btn_y, clear_btn.width+20, clear_btn.height, (106, 209, 4), colors_dict['r']["red3"], 7, 15, border_color=colors_dict['b']['black'], help_text='Grid:')
    grid_toggle_btn.text.font_size = 23
    show_grid = grid_toggle_btn.is_on
    tool_names = ["Cursor", "Eraser"]
    tool_images = [CURSORS["pointer"], CURSORS["eraser"]] # Note: Order must correspond with name order.
    tool_bar = ToolBar(screen, 20, 120, tool_names, tool_images, icon_size=cursor_size)
    tool_bar.selected_tool = "Cursor"
    working_file = None
    tool_bar_width = tool_bar.base_width*tool_bar.draw_scale*tool_bar.width_factor
    tool_bar_height = len(tool_bar.tool_names)*tool_bar.draw_scale*tool_bar.height_factor
    # note: grid argument can also be empty list
    max_canvas_presets = (int((sw - 200)/25), int((sh - 120)/25), 25)
    canvas = Canvas(screen, *(tool_bar_width*4, screen_parts["canvas_pos"][1]+20), *max_canvas_presets, grid=[])
    canvas.drawing_color = color_pallete.selected_color
    select_toggle_btn = ToggleButton(screen, x=tool_bar.x, y=tool_bar_height*3, width=clear_btn.width+20, height=clear_btn.height, on_color=(106, 209, 4), off_color=colors_dict['r']["red3"], border_width=7, border_radius=15, border_color=colors_dict['b']['black'], help_text='Select:' )
    select_mode = select_toggle_btn.is_on
    # scenario: test project loading:
    # open_canvas_from_anp('testFiles/test.anp')
    menu_options_dict = {
        "File":["Open", "Save", "Save As", "New"],
        "Export":["PNG"]
    }
    open_formats = [('Anipixer Working File','*.anp')]
    menu_bar = MenuBar(screen, menu_options_dict=menu_options_dict, bar_height=25, hover_color=(0,0,0), menu_hover_color=WHITE)
    hide_options = False
    buttons = [clear_btn, grid_toggle_btn, select_toggle_btn]
    mpos = pygame.mouse.get_pos()
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONUP: # if the mouse is over the screen, not clicking.
                is_mouse_dragging = False

            if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse was clicked.
                is_mouse_dragging = True
                mpos = pygame.mouse.get_pos()
                # First check tool being used
                tool_bar.get_selected_tool(mpos)
                # always check for color pallete clicks
                color_pallete.get_selected_color(mpos)
                # handles menu bar
                menu_bar.open_menu(mpos)
                
                if menu_bar.is_hovering(mpos):
                    hide_options = False
                else:
                    hide_options = True
                    
                if menu_bar.option_hover(mpos) == True:
                    menu_bar.get_selected_option(mpos)
                    
                """Handling Selected Options from MenuBar"""
                if menu_bar.selected_option == "Open":
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = askopenfilename(title="Open File", filetypes=open_formats)
                    window.destroy()
                    try:
                        screen_title = f"Anpixer - {path_leaf(filename)}" # display filename not full path.
                        canvas.change_data(grid=open_canvas_from_anp(filename))
                        working_file = filename # get the full path
                    except:
                        pass # do not raise error.
                    menu_bar.selected_option = None
                elif menu_bar.selected_option == "Save":
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    if working_file != None:
                        save_canvas_to_anp(canvas, working_file)
                        tkinter.messagebox.showinfo(title="Saved.", message="Your work was saved successfully.")
                        menu_bar.selected_option = None
                    else:
                        tkinter.messagebox.showerror(title="Error.", message="No file has been opened yet.")
                        menu_bar.selected_option = None
                    window.destroy()
                elif menu_bar.selected_option == "Save As":
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = asksaveasfilename(title="Save As File", filetypes=open_formats)
                    window.destroy()
                    try:
                        screen_title = f"Anpixer - {path_leaf(filename)}" # display filename not full path.
                        save_canvas_to_anp(canvas, filename)
                        canvas.change_data(grid=open_canvas_from_anp(filename))
                        working_file = filename # get the full path
                    except:
                        pass # do not raise error.
                    menu_bar.selected_option = None

                # check for toggle buttons
                grid_toggle_btn.toggle(mpos)
                show_grid = grid_toggle_btn.is_on
                select_toggle_btn.toggle(mpos)
                select_mode = select_toggle_btn.is_on
                if tool_bar.selected_tool == "Cursor":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["pointer"]), cursor_size) # change apperance for the tool
                    canvas.drawing_color = color_pallete.selected_color # use color from pallete
                elif tool_bar.selected_tool == "Eraser":
                    cursor = pygame.transform.smoothscale(pygame.image.load(CURSORS["eraser"]), cursor_size)
                    canvas.drawing_color = canvas.canvas_color # use background color attribute of canvas.
                """These Buttons Below Can Be Clicked With Any Tool"""
                if clear_btn.clicked(mpos):
                    canvas.clear_canvas()
                

            elif event.type == pygame.MOUSEMOTION: # checks if the mouse is moving
                mpos = pygame.mouse.get_pos()
                menu_bar.onhover(mpos)
                menu_bar.option_hover(mpos)

            elif event.type == pygame.KEYDOWN:
                # Check for key bindings
                # E.g, Ctrl + S = Save
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    if working_file != None:
                        save_canvas_to_anp(canvas, working_file)
                        tkinter.messagebox.showinfo(title="Saved.", message="Your work was saved successfully.")
                        menu_bar.selected_option = None
                    else:
                        tkinter.messagebox.showerror(title="Error.", message="No file has been opened yet.")
                        menu_bar.selected_option = None
                    window.destroy()
                # E.g, Ctrl + O = Open
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = askopenfilename(title="Open File", filetypes=open_formats)
                    window.destroy()
                    menu_bar.selected_option = None
                    screen_title = f"Anpixer - {path_leaf(filename)}" # display filename not full path.
                    canvas.change_data(grid=open_canvas_from_anp(filename))
                    working_file = filename # get the full path
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    canvas.undo()
                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    canvas.reset()



            elif event.type == VIDEORESIZE: # window resize handler
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                sw, sh = screen.get_width(), screen.get_height()
                max_canvas_presets = (int((sw - 200)/25), int((sh - 120)/25), 25)
                menu_bar.bar_width = sw
                
        if is_mouse_dragging == True: # Mouse draging tools will work here.
            mpos = pygame.mouse.get_pos()
            if tool_bar.selected_tool == "Cursor" or tool_bar.selected_tool == "Eraser":
                canvas.paint_pixel(mpos)
    

        draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar, show_grid, menu_bar, mpos, hide_options, screen_title, select_mode)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

program()

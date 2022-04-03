from pygame_menu import Menu
from Gui.button import Button
from Gui.toggle_button import ToggleButton
from Gui.label import TextNode, TextStyle
from Gui.icon import Icon
from Gui.tool_bar import ToolBar
from Gui.color_pallete import ColorPallete
from Gui.canvas import Canvas
from Utils.utils import *
from Utils.exporter import new_image
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
def draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar, show_grid, mpos, screen_title, select_mode):
    screen.fill(app_background_color) # setting the background color
    pygame.display.set_caption(screen_title)
    for button in buttons: # drawing all buttons
        button.draw(screen)
    # Drawing color pallete
    color_pallete.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15, swatch_outline=WHITE)
    canvas.draw(canvas.grid, canvas.canvas_boundary, show_grid, select_mode)
    tool_bar.draw(outline=True, color=colors_dict['r']['royalblue1'], border_color=colors_dict['b']['black'], border_width=7, border_radius=15)


"""Running Application."""
def program():
    """Runtime Variables"""
    sw, sh = 820, 640
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
    color_pallete_width = len(color_pallete.color_values)*color_pallete.draw_scale*color_pallete.width_factor
    custom_btn_x, custom_btn_y = color_pallete_width+34, color_pallete.y/2+5
    custom_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Custom", 25, WHITE)
    custom_btn = Button(custom_btn_x, custom_btn_y, 120, 55, color=(106, 209, 4), text=custom_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    clear_btn_x, clear_btn_y = color_pallete_width+166,  color_pallete.y/2+5
    clear_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Clear", 25, WHITE)
    clear_btn = Button(clear_btn_x, clear_btn_y, 100, 55, color=colors_dict['r']["red3"], text=clear_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    grid_toggle_btn = ToggleButton(screen, clear_btn_x+clear_btn.width+11, clear_btn_y, clear_btn.width+20, clear_btn.height, (106, 209, 4), colors_dict['r']["red3"], 7, 15, border_color=colors_dict['b']['black'], help_text='Grid:')
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
    select_toggle_btn = ToggleButton(screen, x=tool_bar.x, y=tool_bar_height*2.3, width=clear_btn.width+20, height=clear_btn.height, on_color=(106, 209, 4), off_color=colors_dict['r']["red3"], border_width=7, border_radius=15, border_color=colors_dict['b']['black'], help_text='Select:' )
    select_toggle_btn.text.font_size = 20
    select_mode = select_toggle_btn.is_on
    copy_btn_txt =  TextNode(screen, FONTS["ui_thick_font"], "Copy", 25, WHITE)
    copy_btn = Button(x=tool_bar.x, y=select_toggle_btn.y+clear_btn.height+15, width=clear_btn.width, height=clear_btn.height, color=colors_dict['d']['darkturquoise'], text=copy_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    paste_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Paste", 25, WHITE)
    paste_btn = Button(x=copy_btn.x, y=copy_btn.y+copy_btn.height+15, width=copy_btn.width, height=copy_btn.height, color=(106, 209, 4), text=paste_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    unselect_btn_txt = TextNode(screen, FONTS["ui_thick_font"], "Deselect", 25, WHITE)
    unselect_btn = Button(x=paste_btn.x, y=paste_btn.y+paste_btn.height+15, width=select_toggle_btn.width+5, height=paste_btn.height, color=colors_dict["d"]["darkviolet"], text=unselect_btn_txt, border_width=7, border_radius=15, border_color=colors_dict['b']['black'])
    open_formats = [('Anipixer Working File','*.anp')]
    export_formats = [('PNG', '*.png')]
    buttons = [custom_btn, clear_btn, grid_toggle_btn, select_toggle_btn, copy_btn, paste_btn, unselect_btn]
    unselect_mode = False
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
                if copy_btn.clicked(mpos):
                    if select_mode == True:
                        canvas.copy_from_clipboard()
                if paste_btn.clicked(mpos):
                    if canvas.copied == True:
                        canvas.paste_from_clipboard()
                if unselect_btn.clicked(mpos):
                    canvas.unselect_from_clipboard()

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
                        
                    else:
                        tkinter.messagebox.showerror(title="Error.", message="No file has been opened yet.")
                        
                    window.destroy()
                # E.g, Ctrl + O = Open
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = askopenfilename(title="Open File", filetypes=open_formats)
                    try:
                        screen_title = f"Anpixer - {path_leaf(filename)}" # display filename not full path.
                        canvas.change_data(grid=open_canvas_from_anp(filename))
                        working_file = filename # get the full path
                    except:
                         tkinter.messagebox.showerror(title="Error", message="An error occured when trying to open the file.")
                    window.destroy()
                # Save As
                elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = asksaveasfilename(title="Save As File", filetypes=open_formats)
                    window.destroy()
                    try:
                        save_canvas_to_anp(canvas, filename)
                        screen_title = f"Anpixer - {path_leaf(filename)}" # display filename not full path.
                        canvas.change_data(grid=open_canvas_from_anp(filename))
                        working_file = filename # get the full path
                    except:
                        pass # do not raise error.
                # Copying Pixels to Anipixer's Clipboard
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if select_mode == True:
                        canvas.copy_from_clipboard()
                # Pasting from Anipixer's Clipboard
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if canvas.copied == True:
                        canvas.paste_from_clipboard()
                
                elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    filename = asksaveasfilename(title="Export as PNG", filetypes=export_formats)
                    window.destroy()
                    new_image(canvas.width, canvas.height, canvas.grid)
                    #canvas.pixel_size, [pixel["color"] for pixel in canvas.grid], filename
                # Moving Copied Pixels
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and canvas.copied == True:
                    canvas.move_copied_pixels(direction='up')
                elif keys[pygame.K_s] and canvas.copied == True:
                    canvas.move_copied_pixels(direction='down')
                elif keys[pygame.K_d] and canvas.copied == True:
                    canvas.move_copied_pixels(direction='right')
                elif keys[pygame.K_a] and canvas.copied == True:
                    canvas.move_copied_pixels(direction='left')


            elif event.type == VIDEORESIZE: # window resize handler
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                sw, sh = screen.get_width(), screen.get_height()
                max_canvas_presets = (int((sw - 200)/25), int((sh - 120)/25), 25)
                
        if is_mouse_dragging == True: # Mouse draging tools will work here.
            mpos = pygame.mouse.get_pos()
            if select_mode != True:
                if tool_bar.selected_tool == "Cursor" or tool_bar.selected_tool == "Eraser":
                    canvas.paint_pixel(mpos)
            elif select_mode == True:
                canvas.select_pixels(mpos)

        draw_app(screen, app_background_color, buttons, color_pallete, canvas, tool_bar, show_grid, mpos, screen_title, select_mode)
        draw_cursor(screen, cursor, cursor_rect)
        pygame.display.update()

program()

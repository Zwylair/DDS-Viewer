from sys import argv, exit
from os import remove, getenv, listdir
from os.path import splitext, split, exists
import dearpygui.dearpygui as dpg
from PIL import Image

try:
    if not exists(argv[1]):
        exit()
except BaseException:
    exit()

PATH, file = split(argv[1])


def load_img(file_path: str):
    path, fn = split(file_path)
    filename, ext = splitext(fn)

    img = Image.open(file_path)
    img.save(f'{getenv("tmp")}/{filename}.png')
    width, height, channels, data = dpg.load_image(f'{getenv("tmp")}/{filename}.png')
    remove(f'{getenv("tmp")}/{filename}.png')

    dpg.delete_item('image')
    with dpg.texture_registry():
        texture_tag = dpg.add_static_texture(width=width, height=height, default_value=data)
    
    dpg.add_image(tag='image', texture_tag=texture_tag, pos=[0, 0], parent='window')

    update_items_pos(width, height)
    return width, height


def load_next_img():
    global file

    img_dir = listdir(PATH)
    next_img_id = img_dir.index(file) + 1
    file = img_dir[next_img_id]
    load_img(f'{PATH}/{img_dir[next_img_id]}')


def load_prev_img():
    global file

    img_dir = listdir(PATH)
    next_img_id = img_dir.index(file) - 1
    file = img_dir[next_img_id]

    load_img(f'{PATH}/{img_dir[next_img_id]}')


def update_items_pos(width: int, height: int):
    try:
        dpg.set_viewport_width(width=width + 20)
        dpg.set_viewport_height(height=height + 20)
        dpg.set_item_pos('left_arrow', pos=[5, height + 5])
        dpg.set_item_pos('right_arrow', pos=[30, height + 5])

        dpg.show_item('left_arrow')
        dpg.show_item('right_arrow')
        if listdir(PATH).index(file) == 0:
            dpg.hide_item('left_arrow')
        if listdir(PATH).index(file) == len(listdir(PATH)) - 1:
            dpg.hide_item('right_arrow')
        
        dpg.set_value('image_queue_text', f'({listdir(PATH).index(file) + 1}/{len(listdir(PATH))})')
        dpg.set_value('fn_text', file)
        dpg.set_value('img_width_height_text', f'{width}x{height}')
    except BaseException:
        pass


dpg.create_context()
dpg.create_viewport(title='DDS Viewer', small_icon='icon.ico', large_icon='icon.ico', resizable=False)

with dpg.window(width=2560, height=2560 + 500, no_title_bar=True, no_resize=True, no_close=True, no_move=True, tag='window'):
    width_, height_ = load_img(f'{PATH}/{file}')

    with dpg.group(horizontal=True):
        dpg.add_button(tag='right_arrow', arrow=True, direction=dpg.mvDir_Right, pos=[30, height_ + 5],
                       callback=lambda: load_next_img())
        dpg.add_button(tag='left_arrow', arrow=True, direction=dpg.mvDir_Left, pos=[5, height_ + 5],
                       callback=lambda: load_prev_img())

        if listdir(PATH).index(file) == 0:
            dpg.hide_item('left_arrow')
        if listdir(PATH).index(file) == len(listdir(PATH)) - 1:
            dpg.hide_item('right_arrow')
    
    with dpg.group(horizontal=True):
        dpg.add_text(default_value=file, tag='fn_text')
        dpg.add_text(default_value=f'{width_}x{height_}', tag='img_width_height_text')
        dpg.add_text(default_value=f'({listdir(PATH).index(file) + 1}/{len(listdir(PATH))})', tag='image_queue_text')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

import pyglet
from pyglet.gl import glEnable, GL_TEXTURE_2D

LEFT_MOUSE = pyglet.window.mouse.LEFT
MIDDLE_MOUSE = pyglet.window.mouse.MIDDLE
RIGHT_MOUSE = pyglet.window.mouse.RIGHT

MOD_SHIFT = pyglet.window.key.MOD_SHIFT
MOD_CTRL = pyglet.window.key.MOD_CTRL
MOD_ALT = pyglet.window.key.MOD_ALT

graphics = {
    "window": None,
    "background": None,
    "background_color": None,
    "buffer": None,
    "sprites": [],
    "images": {}
}

handlers = {
    "repeating": [],
}

glEnable(GL_TEXTURE_2D)

def load_images(path):
    pyglet.resource.path = [path]
    images = {}
    images["0"] = pyglet.resource.image("ruutu_tyhja.png")
    for i in range(1, 9):
        images[str(i)] = pyglet.resource.image(f"ruutu_{i}.png")
    images["x"] = pyglet.resource.image("ruutu_miina.png")
    images[" "] = pyglet.resource.image("ruutu_selka.png")
    images["f"] = pyglet.resource.image("ruutu_lippu.png")
    graphics["images"] = images

def create_window(width=800, height=600, background_color=(240, 240, 240, 255)):
    graphics["window"] = pyglet.window.Window(width, height, resizable=True)
    graphics["background_color"] = background_color
    graphics["background"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(background_color).create_image(width, height)
    )

def resize_window(width, height):
    graphics["window"].set_size(width, height)
    graphics["background"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(graphics["background_color"]).create_image(width, height)
    )

def set_mouse_handler(handler):
    if graphics["window"]:
        graphics["window"].on_mouse_press = handler
    else:
        print("Window has not been created!")

def set_keyboard_handler(handler):
    if graphics["window"]:
        graphics["window"].on_key_press = handler
    else:
        print("Window has not been created!")

def set_draw_handler(handler):
    if graphics["window"]:
        graphics["window"].on_draw = handler
    else:
        print("Window has not been created!")

def set_repeat_handler(handler, interval=1/60):
    pyglet.clock.schedule_interval(handler, interval)
    handlers["repeating"].append(handler)

def start():
    pyglet.app.run()

def stop():
    graphics["window"].close()
    graphics["window"] = None
    for handler in handlers["repeating"]:
        pyglet.clock.unschedule(handler)
    pyglet.app.exit()

def clear_window():
    graphics["window"].clear()

def draw_background():
    graphics["background"].draw()

def draw_text(text, x, y, color=(0, 0, 0, 255), font="serif", size=32):
    label = pyglet.text.Label(text,
        font_name=font,
        font_size=size,
        color=color,
        x=x, y=y,
        anchor_x="left", anchor_y="bottom"
    )
    label.draw()

def start_drawing_tiles():
    graphics["buffer"] = pyglet.graphics.Batch()

def add_tile_to_draw(key, x, y):
    graphics["sprites"].append(pyglet.sprite.Sprite(
        graphics["images"][str(key).lower()],
        x,
        y,
        batch=graphics["buffer"]
    ))

def draw_tiles():
    graphics["buffer"].draw()
    graphics["sprites"].clear()

if __name__ == "__main__":
    load_images("sprites")
    create_window()

    def draw():
        clear_window()
        draw_background()
        start_drawing_tiles()
        for i, key in enumerate(graphics["images"].keys()):
            add_tile_to_draw(key, i * 40, 10)
        draw_tiles()

    def close(x, y, button, mods):
        stop()

    set_draw_handler(draw)
    set_mouse_handler(close)
    start()

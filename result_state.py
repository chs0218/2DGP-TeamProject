import game_framework
import title_state
from pico2d import *

image = None
name = "ResultState"

def enter():
    global image
    image = load_image("result/result.png")
    pass


def exit():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(title_state)
    pass


def draw():
    clear_canvas()
    image.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass







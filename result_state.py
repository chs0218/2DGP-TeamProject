import game_framework
import title_state
from pico2d import *

image = None
name = "ResultState"

def enter():
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
    update_canvas()
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass







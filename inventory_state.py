from pico2d import *

import game_framework
import game_world
import server





def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.pop_state()
    pass


def enter():
    pass


def exit():
    pass


def update():
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    server.inventory.draw()
    update_canvas()
    handle_events()
    pass

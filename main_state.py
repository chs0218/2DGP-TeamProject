from pico2d import *

import game_framework
import game_world
import server
import Character
import inventory_state
import inventory

from Dungeon import Dungeon

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_state(inventory_state)
        else:
            server.character.handle_event(event)

    pass


def enter():
    server.golemkamikazeNum = 0
    server.golemsoldierNum = 0
    server.slimeNum = 0
    server.inventory = inventory.Inventory()
    server.character = Character.Character()
    server.dungeon = Dungeon()

    game_world.add_object(server.dungeon, 0)
    game_world.add_object(server.character, 2)



def exit():
    game_world.clear()
    pass


def resume():
    pass


def pause():
    pass


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
    handle_events()
    pass

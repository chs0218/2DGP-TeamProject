from pico2d import *
import random

import game_framework
import game_world
import title_state
import server
import Character
import Slime
import GolemSolider
import Golemkamikaze

from Dungeon import dungeon

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.slime.countexpel()
            server.character.handle_event(event)

    pass


def enter():
    server.character = Character.Character()
    server.slime = Slime.slime()
    server.golemsoldier = GolemSolider.golemsoldier()
    server.golemkamikaze = Golemkamikaze.golemkamikaze()
    server.stage1 = dungeon(3)
    game_world.add_object(server.stage1, 0)
    game_world.add_object(server.slime, 1)
    game_world.add_object(server.golemsoldier, 1)
    game_world.add_object(server.golemkamikaze, 1)
    game_world.add_object(server.character, 2)
    pass


def exit():
    game_world.clear()
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

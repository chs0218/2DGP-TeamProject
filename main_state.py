from pico2d import *
import random

import game_framework
import game_world
import title_state
import Character
import Slime
import GolemSolider
import Golemkamikaze

from Dungeon import dungeon

difficulty = None
character = None
slime = None
golemsoldier = None
golemkamikaze = None
cur_stage = None
stage1 = None
stage2 = None
stage3 = None


def handle_events():
    global KeyBoardDic, character, slime, stage1
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            stage1.isClear = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2 and stage1.isClear:
            stage1.isClear = False
            stage1.DoorAnimation = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            character.cur_state = Character.IdleState
            character.hp = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            slime.countexpel()
            character.handle_event(event)

    pass


def enter():
    global character, slime, stage1, stage2, stage3, cur_stage, difficulty, golemsoldier
    global golemkamikaze
    difficulty = title_state.difficulty
    character = Character.Character()
    slime = Slime.slime()
    golemsoldier = GolemSolider.golemsoldier()
    golemkamikaze = Golemkamikaze.golemkamikaze()
    stage1 = dungeon(3)
    stage2 = dungeon(5)
    stage3 = dungeon(7)
    cur_stage = stage1
    game_world.add_object(stage1, 0)
    game_world.add_object(slime, 1)
    game_world.add_object(golemsoldier, 1)
    game_world.add_object(golemkamikaze, 1)
    game_world.add_object(character, 2)
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

from pico2d import *
import random
import game_framework
import title_state
import Character
import Slime
import GolemSolider
from Dungeon import dungeon
from Monster import *

difficulty = None
character = None
slime = None
golemsoldier = None
golemkamikaze = None
IsClear = False
dungeons = None
AnimationClock = 0
SlimeNum = 0

def check_attack():
    LeftX = character.x - 50
    LeftY = character.y - 50
    RightX = character.x + 50
    RightY = character.y + 50

    if character.dir == 0:
        pass
    elif character.dir == 1:
        pass
    elif character.dir == 2:
        pass
    else:
        pass

    for i in range(SlimeNum):
        if LeftX < slime[i].x < RightX and LeftY < slime[i].y < RightY:
            slime[i].hp -= 1
            if slime[i].hp == 0:
                slime[i].dead = True
    if LeftX < golemsoldier.x < RightX and LeftY < golemsoldier.y < RightY:
        golemsoldier.hp -= 1
        if golemsoldier.hp == 0:
            golemsoldier.dead = True


def handle_events():
    global IsClear, KeyBoardDic, character, slime
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            slime.countexpel()
            character.handle_event(event)

    pass


def enter():
    global character, slime, dungeons, difficulty, SlimeNum, golemsoldier
    #global golemkamikaze
    difficulty = title_state.difficulty
    SlimeNum = 4
    character = Character.Character()
    slime = Slime.slime()
    golemsoldier = GolemSolider.golemsoldier()
    # golemkamikaze = Golemkamikaze()
    dungeons = dungeon()
    pass


def exit():
    global character, dungeons, slime, golemsoldier, golemkamikaze
    del character, dungeons, slime, golemsoldier, golemkamikaze
    pass


def update():
    global AnimationClock
    global character, slime, golemsoldier, golemkamikaze
    character.update()
    slime.update()
    golemsoldier.update()
    # if AnimationClock % 20 == 0:
    #     for i in range(SlimeNum):
    #         if not slime[i].dead:
    #             slime[i].update_animation()
    #     if not golemsoldier.dead:
    #         golemsoldier.update_animation()
    #     if not golemkamikaze.bomb:
    #         golemkamikaze.update_animation()
    # for i in range(SlimeNum):
    #     if not slime[i].dead:
    #         slime[i].move(character)
    # if not golemsoldier.dead:
    #     golemsoldier.move(character)
    # if not golemkamikaze.bomb:
    #     golemkamikaze.move(character)
    # AnimationClock = (AnimationClock + 1) % 100


def draw():
    clear_canvas()
    dungeons.draw()
    slime.draw()
    golemsoldier.draw()
    # for i in range(SlimeNum):
    #     if slime[i].dead:
    #         slime[i].draw()
    # if golemkamikaze.bomb:
    #     golemkamikaze.draw()
    # golemsoldier.draw()
    # if not golemkamikaze.bomb:
    #     golemkamikaze.draw()
    # for i in range(SlimeNum):
    #     if not slime[i].expelCount and not slime[i].dead:
    #         slime[i].draw()
    # for i in range(SlimeNum):
    #     if not slime[i].dead and slime[i].expelCount:
    #         slime[i].draw()

    character.draw()
    update_canvas()
    handle_events()
    pass

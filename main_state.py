from pico2d import *
import random
import game_framework
import title_state
from Dungeon import dungeon
from Monster import *

KeyBoardDic = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'j': False, 'k': False}

difficulty = None
character = None
slime = None
golemsoldier = None
golemkamikaze = None
IsClear = False
dungeons = None
AnimationClock = 0
SlimeNum = 0

class Character:
    def __init__(self):
        self.x = 630
        self.y = 120
        self.combo = 0
        self.state = 8
        self.block = 1
        self.Roll = load_image("player/player_roll.png")
        self.Die = load_image("player/Player_Die.png")
        self.Idle = load_image("player/player_idle.png")
        self.Walk = load_image("player/player_walk.png")
        self.Attack = load_image("player/player_attack.png")
        self.Shield = load_image("player/player_shield_defense.png")
        self.ShieldMove = load_image("player/player_shield_walk.png")
        self.animation = 0
        self.dir = 0

    def draw(self):
        if self.state == 0:
            self.Roll.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 1:
            if self.dir > 1:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y - 15)
            else:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y)
        elif self.state == 2:
            self.Shield.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 3:
            self.ShieldMove.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 4:
            self.Walk.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        else:
            self.Idle.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)

    def update_animation(self):
        if self.state == 0:
            if self.animation == 7:
                KeyBoardDic.update(space=False)
            self.animation = (self.animation + 1) % 8
        elif self.state == 1:
            if self.combo == 1:
                if self.animation > 3:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 5
                pass
            elif self.combo == 2:
                if self.animation > 7:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 9
            else:
                if self.animation > 16:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 18

            if self.animation == 3 or self.animation == 7 or self.animation == 12:
                check_attack()
        elif self.state == 2:
            self.animation = (self.animation + 1) % self.block
        elif 2 < self.state < 6:
            self.animation = (self.animation + 1) % 8

    def update_state(self):
        if KeyBoardDic['space']:
            self.state = 0
        elif KeyBoardDic['j']:
            self.state = 1
        elif KeyBoardDic['k']:
            if KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
                self.state = 3
            else:
                if self.animation > 5:
                    self.animation = 0
                self.state = 2
        elif KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
            self.state = 4
        else:
            self.state = 5

        if not self.state == 1:
            if KeyBoardDic['w']:
                self.dir = 0
            elif KeyBoardDic['s']:
                self.dir = 1
            elif KeyBoardDic['a']:
                self.dir = 2
            elif KeyBoardDic['d']:
                self.dir = 3

    def update_character(self):
        if self.state == 0:
            self.move(1.5)
        elif self.state == 1:
            if self.animation == 1:
                self.move(2)
            elif self.animation == 6:
                self.move(2)
            elif self.animation == 10:
                self.move(1.5)
            pass
        elif self.state == 3:
            self.move(0.5)
            pass
        elif self.state == 4:
            self.move(1)
            pass
        else:
            pass

    def move(self, i):
        if self.dir == 0:
            if self.y < get_canvas_height() - 80:
                self.y += i
            else:
                self.y = get_canvas_height() - 80
        elif self.dir == 1:
            if self.y > 120:
                self.y -= i
            else:
                self.y = 120
        elif self.dir == 2:
            if self.x > 160:
                self.x -= i
            else:
                self.x = 160
        elif self.dir == 3:
            if self.x < get_canvas_width() - 160:
                self.x += i
            else:
                self.x = get_canvas_width() - 160


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

def check_slime():
    for i in range(SlimeNum):
        slime[i].countexpel()
    pass


def handle_events():
    global IsClear, KeyBoardDic, character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_w:
                check_slime()
                KeyBoardDic.update(w=True)
            elif event.key == SDLK_s:
                check_slime()
                KeyBoardDic.update(s=True)
            elif event.key == SDLK_a:
                check_slime()
                KeyBoardDic.update(a=True)
            elif event.key == SDLK_d:
                check_slime()
                KeyBoardDic.update(d=True)
            elif event.key == SDLK_SPACE:
                check_slime()
                if not character.state == 0:
                    character.animation = 0
                KeyBoardDic.update(space=True)
                KeyBoardDic.update(j=False)
                character.combo = 0
            elif event.key == SDLK_j:
                if not character.state == 0 and not character.state == 1:
                    character.animation = 0
                character.combo += 1
                KeyBoardDic.update(j=True)
            elif event.key == SDLK_k:
                if not character.state == 1:
                    character.animation = 0
                KeyBoardDic.update(k=True)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_k:
                KeyBoardDic.update(k=False)
            elif event.key == SDLK_w:
                KeyBoardDic.update(w=False)
            elif event.key == SDLK_s:
                KeyBoardDic.update(s=False)
            elif event.key == SDLK_a:
                KeyBoardDic.update(a=False)
            elif event.key == SDLK_d:
                KeyBoardDic.update(d=False)

    pass


def enter():
    global character, slime, dungeons, difficulty, SlimeNum, golemsoldier
    global golemkamikaze
    difficulty = title_state.difficulty
    SlimeNum = 4
    character = Character()
    slime = [Slime() for i in range(SlimeNum)]
    golemsoldier = GolemSoldier()
    golemkamikaze = Golemkamikaze()
    dungeons = dungeon()
    pass


def exit():
    global character, dungeons, slime, golemsoldier, golemkamikaze
    del character, dungeons, slime, golemsoldier, golemkamikaze
    pass


def update():
    global AnimationClock
    global character, slime, golemsoldier, golemkamikaze
    if AnimationClock % 20 == 0:
        character.update_animation()
        for i in range(SlimeNum):
            if not slime[i].dead:
                slime[i].update_animation()
        if not golemsoldier.dead:
            golemsoldier.update_animation()
        if not golemkamikaze.bomb:
            golemkamikaze.update_animation()

    character.update_state()
    character.update_character()
    for i in range(SlimeNum):
        if not slime[i].dead:
            slime[i].move(character)
    if not golemsoldier.dead:
        golemsoldier.move(character)
    if not golemkamikaze.bomb:
        golemkamikaze.move(character)
    AnimationClock = (AnimationClock + 1) % 100


def draw():
    clear_canvas()
    dungeons.draw()
    for i in range(SlimeNum):
        if slime[i].dead:
            slime[i].draw()
    if golemkamikaze.bomb:
        golemkamikaze.draw()
    golemsoldier.draw()
    if not golemkamikaze.bomb:
        golemkamikaze.draw()
    for i in range(SlimeNum):
        if not slime[i].expelCount and not slime[i].dead:
            slime[i].draw()
    character.draw()
    for i in range(SlimeNum):
        if not slime[i].dead and slime[i].expelCount:
            slime[i].draw()
    update_canvas()
    handle_events()
    pass

from pico2d import *
import game_framework
import title_state

KeyBoardDic = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'j': False, 'k': False}

character = None
IsClear = False
DungeonBK = None
DungeonBK2 = None
DungeonDoor = None
DoorAnimation = 0
AnimationClock = 0


class Character:
    def __init__(self):
        self.x = 600
        self.y = 350
        self.state = 8
        self.block = 1
        self.Roll = load_image("player/player_roll.png")
        self.Die = load_image("player/Player_Die.png")
        self.Idle = load_image("player/player_idle.png")
        self.Walk = load_image("player/player_walk.png")
        self.Attack = load_image("player/player_attack.png")
        self.Shield = load_image("player/player_shield_defense.png")
        self.animation = 0
        self.dir = 0

    def draw(self):
        if self.state == 0:
            self.Roll.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 1:
            self.Shield.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 2:
            if self.dir > 1:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y - 15)
            else:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y)

        elif 2 < self.state < 7:
            self.Walk.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        else:
            self.Idle.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)

    def update_animation(self):
        if self.state == 0:
            if self.animation == 7:
                KeyBoardDic.update(space=False)
            self.animation = (self.animation + 1) % 8
        elif self.state == 1:
            self.animation = (self.animation + 1) % self.block
        elif self.state == 2:
            if self.animation > 16:
                KeyBoardDic.update(j=False)
            self.animation = (self.animation + 1) % 18

        elif 2 < self.state < 9:
            self.animation = (self.animation + 1) % 8

    def update_state(self):

        if KeyBoardDic['space']:
            KeyBoardDic.update(j=False)
            self.state = 0

        elif KeyBoardDic['k']:
            KeyBoardDic.update(j=False)
            self.state = 1

        elif KeyBoardDic['j']:
            self.state = 2

        elif KeyBoardDic['w']:
            self.state = 3

        elif KeyBoardDic['s']:
            self.state = 4

        elif KeyBoardDic['a']:
            self.state = 5

        elif KeyBoardDic['d']:
            self.state = 6

        else:
            self.state = 7

    def update_character(self):
        if self.state == 0:
            if self.dir == 0:
                if self.y < get_canvas_height() - 80:
                    self.y += 1.5

            elif self.dir == 1:
                if self.y > 120:
                    self.y -= 1.5

            elif self.dir == 2:
                if self.x > 160:
                    self.x -= 1.5

            elif self.dir == 3:
                if self.x < get_canvas_width() - 160:
                    self.x += 1.5

        elif self.state == 3:
            self.dir = 0
            if self.y < get_canvas_height() - 80:
                self.y += 1

        elif self.state == 4:
            self.dir = 1
            if self.y > 120:
                self.y -= 1

        elif self.state == 5:
            self.dir = 2
            if self.x > 160:
                self.x -= 1

        elif self.state == 6:
            self.dir = 3
            if self.x < get_canvas_width() - 160:
                self.x += 1


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
                KeyBoardDic.update(w=True)
            elif event.key == SDLK_s:
                KeyBoardDic.update(s=True)
            elif event.key == SDLK_a:
                KeyBoardDic.update(a=True)
            elif event.key == SDLK_d:
                KeyBoardDic.update(d=True)
            elif event.key == SDLK_SPACE:
                if not character.animation == 0:
                    character.animation = 0
                KeyBoardDic.update(space=True)
            elif event.key == SDLK_j:
                if not character.state == 2:
                    character.animation = 0
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
    global character, DungeonBK, DungeonBK2, DungeonDoor
    character = Character()
    DungeonBK = load_image("map/Dungeon_BK.png")
    DungeonBK2 = load_image("map/BKWalls.png")
    DungeonDoor = load_image("map/Door.png")
    pass


def exit():
    global character, DungeonBK, DungeonBK2, DungeonDoor
    del character, DungeonBK, DungeonBK2, DungeonDoor
    pass


def update():
    global AnimationClock
    global character
    if AnimationClock % 15 == 0:
        character.update_animation()

    character.update_state()
    character.update_character()

    AnimationClock = (AnimationClock + 1) % 100


def draw():
    clear_canvas()
    DungeonBK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    DungeonBK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    DungeonDoor.clip_draw(200 * DoorAnimation, 0, 200, 200, get_canvas_width() // 2, get_canvas_height() - 60)
    character.draw()
    update_canvas()
    handle_events()
    pass

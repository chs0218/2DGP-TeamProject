from pico2d import *

W_UP, W_DOWN, S_UP, S_DOWN, A_UP, A_DOWN, D_UP, D_DOWN, \
J_UP, J_DOWN, K_UP, K_DOWN, SPACE_UP, SPACE_DOWN = range(14)

key_event_table = {
    (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYDOWN, SDLK_w): W_DOWN,
    (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYDOWN, SDLK_s): S_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYUP, SDLK_w): J_UP,
    (SDL_KEYDOWN, SDLK_w): J_DOWN,
    (SDL_KEYUP, SDLK_w): K_UP,
    (SDL_KEYDOWN, SDLK_w): K_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
}

class IdleState:
    pass

class MoveState:
    pass

class AttackState:
    pass

class DefenceState:
    pass

class DefenceWalkState:
    pass

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
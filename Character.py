import game_framework
from pico2d import *

W_UP, W_DOWN, S_UP, S_DOWN, A_UP, A_DOWN, D_UP, D_DOWN, \
J_DOWN, K_UP, K_DOWN, SPACE_DOWN, UPDATE_STATE = range(13)

event_name = ['W_UP', 'W_DOWN', 'S_UP', 'S_DOWN', 'A_UP', 'A_DOWN', 'D_UP', 'D_DOWN',
              'J_DOWN', 'K_UP', 'K_DOWN', 'SPACE_DOWN', 'UPDATE_STATE']

PIXEL_PER_METER = (100.0 / 1.8)
RUN_SPEED_KMPH = 20.0
AVOID_SPEED_KMPH = 30.0
ATTACK_SPEED_KMPH = 30.0
DEFENSE_SPEED_KMPH = 10.0

RUN_SPEED_PPS = ((RUN_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER)
AVOID_SPEED_PPS = ((AVOID_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER)
ATTACK_SPEED_PPS = ((ATTACK_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER)
DEFENSE_SPEED_PPS = ((DEFENSE_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER)

key_event_table = {
    (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYDOWN, SDLK_w): W_DOWN,
    (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYDOWN, SDLK_s): S_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYDOWN, SDLK_j): J_DOWN,
    (SDL_KEYUP, SDLK_k): K_UP,
    (SDL_KEYDOWN, SDLK_k): K_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
}


class IdleState:
    def enter(Character, event):
        if Character.pre_state != Character.cur_state:
            Character.animation = 0
        pass

    def exit(Character, event):
        pass

    def do(Character):
        Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time) % 10
        pass

    def draw(Character):
        Character.Idle.clip_draw(100 * int(Character.animation), 100 * Character.dir,
                                 100, 100, Character.x, Character.y)
        pass


class MoveState:
    def enter(Character, event):
        pass


    def exit(Character, event):
        pass

    def do(Character):
        Character.move(RUN_SPEED_PPS)
        Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time) % 8
        pass

    def draw(Character):
        Character.Walk.clip_draw(100 * int(Character.animation), 100 * Character.dir,
                                 100, 100, Character.x, Character.y)
        pass


class AvoidState:
    def enter(Character, event):
        pass

    def exit(Character, event):
        pass

    def do(Character):
        Character.move(AVOID_SPEED_PPS)
        Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time)
        if Character.animation > 8:
            Character.KeyBoardDic.update(space=False)
            Character.add_event(UPDATE_STATE)

        Character.animation %= 8
        pass

    def draw(Character):
        Character.Roll.clip_draw(100 * int(Character.animation), 100 * Character.dir,
                                 100, 100, Character.x, Character.y)
        pass


class AttackState:
    def enter(Character, event):
        pass

    def exit(Character, event):
        pass

    def do(Character):
        if Character.combo == 1:
            Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time)

            if Character.animation > 5:
                Character.KeyBoardDic.update(j=False)
                Character.add_event(UPDATE_STATE)
                Character.combo = 0

            Character.animation %= 5
            pass
        elif Character.combo == 2:
            Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time)

            if Character.animation > 9:
                Character.KeyBoardDic.update(j=False)
                Character.add_event(UPDATE_STATE)
                Character.combo = 0

            Character.animation %= 9
        else:
            Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time)
            if Character.animation > 18:
                Character.KeyBoardDic.update(j=False)
                Character.add_event(UPDATE_STATE)
                Character.combo = 0

            Character.animation %= 18

        if Character.animation == 3 or Character.animation == 7 or Character.animation == 12:
            # 공격 체크
            pass
        elif 1 < Character.animation < 2:
            Character.move(ATTACK_SPEED_PPS)
        elif 6 < Character.animation < 7:
            Character.move(ATTACK_SPEED_PPS)
        elif 10 < Character.animation < 11:
            Character.move(ATTACK_SPEED_PPS)
        pass

    def draw(Character):
        if Character.dir > 0:
            Character.Attack.clip_draw(400 * int(Character.animation), 400 * Character.dir,
                                       400, 400, Character.x, Character.y - 15)
        else:
            Character.Attack.clip_draw(400 * int(Character.animation), 400 * Character.dir,
                                       400, 400, Character.x, Character.y)
        pass


class DefenceState:
    def enter(Character, event):
        pass

    def exit(Chracter, event):
        pass

    def do(Character):
        Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME
                               * game_framework.frame_time) % Character.block
        pass

    def draw(Character):
        Character.Shield.clip_draw(100 * int(Character.animation), 100 * Character.dir,
                                   100, 100, Character.x, Character.y)
        pass
    pass


class DefenceWalkState:
    def enter(Character, event):
        pass

    def exit(Chracter, event):
        pass

    def do(Character):
        Character.move(DEFENSE_SPEED_PPS)
        Character.animation = (Character.animation + game_framework.FRAMES_PER_TIME * game_framework.frame_time) % 8
        pass

    def draw(Character):
        Character.ShieldMove.clip_draw(100 * int(Character.animation), 100 * Character.dir,
                                   100, 100, Character.x, Character.y)
        pass


class Character:
    def __init__(self):
        self.x = 630
        self.y = 120
        self.combo = 0
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
        self.event_que = []
        self.KeyBoardDic = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'j': False, 'k': False}
        self.cur_state = IdleState
        self.pre_state = IdleState

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.updateKeyBoardDic(event)
            self.pre_state = self.cur_state
            self.cur_state.exit(self, event)
            self.updateState()
            if self.pre_state != self.cur_state:
                self.animation = 0
            self.cur_state.enter(self, event)

    def updateKeyBoardDic(self, event):
        if event == W_UP:
            self.KeyBoardDic.update(w=False)
        elif event == W_DOWN:
            self.KeyBoardDic.update(w=True)
        elif event == S_UP:
            self.KeyBoardDic.update(s=False)
        elif event == S_DOWN:
            self.KeyBoardDic.update(s=True)
        elif event == A_UP:
            self.KeyBoardDic.update(a=False)
        elif event == A_DOWN:
            self.KeyBoardDic.update(a=True)
        elif event == D_UP:
            self.KeyBoardDic.update(d=False)
        elif event == D_DOWN:
            self.KeyBoardDic.update(d=True)
        elif event == J_DOWN:
            self.KeyBoardDic.update(j=True)
            self.combo += 1
        elif event == K_UP:
            self.KeyBoardDic.update(k=False)
        elif event == K_DOWN:
            self.KeyBoardDic.update(k=True)
        elif event == SPACE_DOWN:
            self.KeyBoardDic.update(space=True)
            self.KeyBoardDic.update(j=False)

    def updateState(self):
        if self.KeyBoardDic['space']:
            self.cur_state = AvoidState

        elif self.KeyBoardDic['j']:
            self.cur_state = AttackState

        elif self.KeyBoardDic['k']:
            if self.KeyBoardDic['w'] or self.KeyBoardDic['s'] or self.KeyBoardDic['a'] or self.KeyBoardDic['d']:
                self.cur_state = DefenceWalkState
            else:
                self.cur_state = DefenceState
        elif self.KeyBoardDic['w'] or self.KeyBoardDic['s'] or self.KeyBoardDic['a'] or self.KeyBoardDic['d']:
            self.cur_state = MoveState
        else:
            self.cur_state = IdleState

        if not self.cur_state == AttackState and not self.cur_state == AvoidState:
            if self.KeyBoardDic['w']:
                self.dir = 0
            elif self.KeyBoardDic['s']:
                self.dir = 1
            elif self.KeyBoardDic['a']:
                self.dir = 2
            elif self.KeyBoardDic['d']:
                self.dir = 3

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def move(self, speed):
        if self.dir == 0:
            self.y += speed * game_framework.frame_time
            self.y = clamp(120, self.y, get_canvas_height() - 80)
        elif self.dir == 1:
            self.y -= speed * game_framework.frame_time
            self.y = clamp(120, self.y, get_canvas_height() - 80)
        elif self.dir == 2:
            self.x -= speed * game_framework.frame_time
            self.x = clamp(165, self.x, get_canvas_width() - 165)
        elif self.dir == 3:
            self.x += speed * game_framework.frame_time
            self.x = clamp(165, self.x, get_canvas_width() - 165)
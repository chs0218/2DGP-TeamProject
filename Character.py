from pico2d import *

W_UP, W_DOWN, S_UP, S_DOWN, A_UP, A_DOWN, D_UP, D_DOWN, \
J_UP, J_DOWN, K_UP, K_DOWN, SPACE_UP, SPACE_DOWN, ATTACK_END_IDLE, \
ATTACK_END_MOVE, AVOID_END_IDLE, AVOID_END_MOVE = range(18)

event_name = ['W_UP', 'W_DOWN', 'S_UP', 'S_DOWN', 'A_UP', 'A_DOWN', 'D_UP', 'D_DOWN', \
'J_UP', 'J_DOWN', 'K_UP', 'K_DOWN', 'SPACE_UP', 'SPACE_DOWN', 'ATTACK_END_IDLE', \
'ATTACK_END_MOVE', 'AVOID_END_IDLE', 'AVOID_END_MOVE']

key_event_table = {
    (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYDOWN, SDLK_w): W_DOWN,
    (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYDOWN, SDLK_s): S_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYUP, SDLK_j): J_UP,
    (SDL_KEYDOWN, SDLK_j): J_DOWN,
    (SDL_KEYUP, SDLK_k): K_UP,
    (SDL_KEYDOWN, SDLK_k): K_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
}


def SetDir(Character, event):
    if event == W_DOWN:
        Character.UpDowndir += 1

    elif event == S_DOWN:
        Character.UpDowndir -= 1

    elif event == A_DOWN:
        Character.LeftRightdir -= 1

    elif event == D_DOWN:
        Character.LeftRightdir += 1

    elif event == W_UP:
        Character.UpDowndir -= 1

    elif event == S_UP:
        Character.UpDowndir += 1

    elif event == A_UP:
        Character.LeftRightdir += 1

    elif event == D_UP:
        Character.LeftRightdir -= 1


class IdleState:
    def enter(Character, event):
        if Character.pre_state != IdleState:
            Character.animation = 0
        SetDir(Character, event)
        Character.update_dir()

    def exit(Character, event):
        pass

    def do(Chracter):
        Chracter.animation = (Chracter.animation + 1) % 8
        pass

    def draw(Character):
        Character.Idle.clip_draw(100 * Character.animation, 100 * Character.dir, 100, 100, Character.x, Character.y)
        pass


class MoveState:
    def enter(Character, event):
        if Character.pre_state != MoveState:
            Character.animation = 0

        SetDir(Character, event)
        Character.update_dir()


    def exit(Character, event):
        pass

    def do(Chracter):
        Chracter.animation = (Chracter.animation + 1) % 8
        pass

    def draw(Character):
        Character.Walk.clip_draw(100 * Character.animation, 100 * Character.dir, 100, 100, Character.x, Character.y)
        pass


class AvoidState:
    def enter(Character, event):
        if Character.pre_state != AvoidState:
            Character.animation = 0
        SetDir(Character, event)
        Character.update_dir()

    def exit(Character, event):
        pass

    def do(Chracter):
        if Chracter.animation == 7:
            if (Chracter.UpDowndir + Chracter.LeftRightdir) == 0:
                Chracter.add_event(AVOID_END_IDLE)
            else:
                Chracter.add_event(AVOID_END_MOVE)
        Chracter.animation = (Chracter.animation + 1) % 8
        print(Chracter.UpDowndir + Chracter.LeftRightdir)
        pass

    def draw(Character):
        Character.Roll.clip_draw(100 * Character.animation, 100 * Character.dir, 100, 100, Character.x, Character.y)
        pass


class AttackState:
    def enter(Character, event):
        if Character.pre_state != AttackState:
            Character.animation = 0
            Chracter.combo = 0
        if event == J_DOWN and Character.combo < 3:
            Character.combo += 1
        SetDir(Character, event)
        pass

    def exit(Character, event):
        if event == ATTACK_END_IDLE:
            Character.combo = 0

        elif event == ATTACK_END_MOVE:
            Character.combo = 0
        pass

    def do(Character):
        if Character.combo == 1:
            if Character.animation > 3:
                if (Character.UpDowndir + Character.LeftRightdir) == 0:
                    Character.add_event(ATTACK_END_IDLE)
                elif (Character.UpDowndir + Character.LeftRightdir) == 2:
                    Character.add_event(ATTACK_END_IDLE)
                elif (Character.UpDowndir + Character.LeftRightdir) == -2:
                    Character.add_event(ATTACK_END_IDLE)
                else:
                    Character.add_event(ATTACK_END_MOVE)
                Character.combo = 0
            Character.animation = (Character.animation + 1) % 5
            pass
        elif Character.combo == 2:
            if Character.animation > 7:
                if (Character.UpDowndir + Character.LeftRightdir) == 0 or \
                        (Character.UpDowndir + Character.LeftRightdir) == 2 or \
                        (Character.UpDowndir + Character.LeftRightdir) == -2:
                    Character.add_event(ATTACK_END_IDLE)
                else:
                    Character.add_event(ATTACK_END_MOVE)
                Character.combo = 0
            Character.animation = (Character.animation + 1) % 9
        else:
            if Character.animation > 16:
                if (Character.UpDowndir + Character.LeftRightdir) == 0 or \
                        (Character.UpDowndir + Character.LeftRightdir) == 2 or \
                        (Character.UpDowndir + Character.LeftRightdir) == -2:
                    Character.add_event(ATTACK_END_IDLE)
                else:
                    Character.add_event(ATTACK_END_MOVE)
                Character.combo = 0
            Character.animation = (Character.animation + 1) % 18

        if Character.animation == 3 or Character.animation == 7 or Character.animation == 12:
            # 공격 체크
            pass
        pass

    def draw(Character):
        if Character.dir > 1:
            Character.Attack.clip_draw(400 * Character.animation, 400 * Character.dir,
                                       400, 400, Character.x, Character.y - 15)
        else:
            Character.Attack.clip_draw(400 * Character.animation, 400 * Character.dir,
                                       400, 400, Character.x, Character.y)
        pass


class DefenceState:
    def enter(Character, event):
        if Character.pre_state != DefenceState:
            Character.animation = 0

        SetDir(Character, event)
        Character.update_dir()

    def exit(Chracter, event):
        pass

    def do(Chracter):
        Chracter.animation = (Chracter.animation + 1) % Chracter.block
        pass

    def draw(Character):
        Character.Shield.clip_draw(100 * Character.animation, 100 * Character.dir,
                                   100, 100, Character.x, Character.y)
        pass
    pass


class DefenceWalkState:
    def enter(Character, event):
        if Character.pre_state != DefenceWalkState:
            Character.animation = 0

        SetDir(Character, event)
        Character.update_dir()

    def exit(Chracter, event):
        pass

    def do(Chracter):
        Chracter.animation = (Chracter.animation + 1) % 8
        pass

    def draw(Character):
        Character.ShieldMove.clip_draw(100 * Character.animation, 100 * Character.dir,
                                   100, 100, Character.x, Character.y)
        pass


next_state_table = {
    IdleState: {W_UP: MoveState, W_DOWN: MoveState,
                S_UP: MoveState, S_DOWN: MoveState,
                A_UP: MoveState, A_DOWN: MoveState,
                D_UP: MoveState, D_DOWN: MoveState,
                J_UP: IdleState, J_DOWN: AttackState,
                K_UP: IdleState, K_DOWN: DefenceState,
                SPACE_UP: IdleState, SPACE_DOWN: AvoidState,

                },

    MoveState:  {W_UP: IdleState, W_DOWN: IdleState,
                S_UP: IdleState, S_DOWN: IdleState,
                A_UP: IdleState, A_DOWN: IdleState,
                D_UP: IdleState, D_DOWN: IdleState,
                J_UP: IdleState, J_DOWN: AttackState,
                K_UP: IdleState, K_DOWN: DefenceWalkState,
                SPACE_UP: IdleState, SPACE_DOWN: AvoidState
                },

    AvoidState:  {W_UP: AvoidState, W_DOWN: AvoidState,
                S_UP: AvoidState, S_DOWN: AvoidState,
                A_UP: AvoidState, A_DOWN: AvoidState,
                D_UP: AvoidState, D_DOWN: AvoidState,
                J_UP: AvoidState, J_DOWN: AvoidState,
                K_UP: AvoidState, K_DOWN: AvoidState,
                SPACE_UP: AvoidState, SPACE_DOWN: AvoidState,
                AVOID_END_IDLE: IdleState, AVOID_END_MOVE: MoveState
                },

    AttackState:  {W_UP: AttackState, W_DOWN: AttackState,
                S_UP: AttackState, S_DOWN: AttackState,
                A_UP: AttackState, A_DOWN: AttackState,
                D_UP: AttackState, D_DOWN: AttackState,
                J_UP: AttackState, J_DOWN: AttackState,
                K_UP: AttackState, K_DOWN: AttackState,
                SPACE_UP: AttackState, SPACE_DOWN: AttackState,
                ATTACK_END_IDLE: IdleState, ATTACK_END_MOVE: MoveState
                },

    DefenceState: {W_UP: DefenceWalkState, W_DOWN: DefenceWalkState,
                S_UP: DefenceWalkState, S_DOWN: DefenceWalkState,
                A_UP: DefenceWalkState, A_DOWN: DefenceWalkState,
                D_UP: DefenceWalkState, D_DOWN: DefenceWalkState,
                J_UP: DefenceState, J_DOWN: AttackState,
                K_UP: IdleState, K_DOWN: DefenceState,
                SPACE_UP: AvoidState, SPACE_DOWN: AvoidState
                },

    DefenceWalkState: {W_UP: DefenceState, W_DOWN: DefenceState,
                S_UP: DefenceState, S_DOWN: DefenceState,
                A_UP: DefenceState, A_DOWN: DefenceState,
                D_UP: DefenceState, D_DOWN: DefenceState,
                J_UP: DefenceWalkState, J_DOWN: AttackState,
                K_UP: MoveState, K_DOWN: DefenceWalkState,
                SPACE_UP: AvoidState, SPACE_DOWN: AvoidState
                }
}


class Chracter:
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
        self.UpDowndir = 0
        self.LeftRightdir = 0
        self.dir = 0
        self.event_que = []
        self.cur_state = IdleState
        self.pre_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update_dir(self):
        if self.UpDowndir == 1:
            self.dir = 0
        elif self.UpDowndir == -1:
            self.dir = 1
        elif self.LeftRightdir == -1:
            self.dir = 2
        elif self.LeftRightdir == 1:
            self.dir = 3
        # print(self.UpDowndir)
        # print(self.LeftRightdir)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.pre_state = self.cur_state
                self.cur_state = next_state_table[self.cur_state][event]
                # print('State:', self.cur_state.__name__, 'Event:', event_name[event])

            except:
                print('State:', self.cur_state.__name__, 'Event:', event_name[event])
                exit(-1)  # 강제 종료

            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)



# class Character:
#     def __init__(self):
#         self.x = 630
#         self.y = 120
#         self.combo = 0
#         self.state = 8
#         self.block = 1
#         self.Roll = load_image("player/player_roll.png")
#         self.Die = load_image("player/Player_Die.png")
#         self.Idle = load_image("player/player_idle.png")
#         self.Walk = load_image("player/player_walk.png")
#         self.Attack = load_image("player/player_attack.png")
#         self.Shield = load_image("player/player_shield_defense.png")
#         self.ShieldMove = load_image("player/player_shield_walk.png")
#         self.animation = 0
#         self.dir = 0
#
#     def draw(self):
#         if self.state == 0:
#             self.Roll.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
#         elif self.state == 1:
#             if self.dir > 1:
#                 self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y - 15)
#             else:
#                 self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y)
#         elif self.state == 2:
#             self.Shield.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
#         elif self.state == 3:
#             self.ShieldMove.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
#         elif self.state == 4:
#             self.Walk.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
#         else:
#             self.Idle.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
#
#     def update_animation(self):
#         if self.state == 0:
#             if self.animation == 7:
#                 KeyBoardDic.update(space=False)
#             self.animation = (self.animation + 1) % 8
#         elif self.state == 1:
#             if self.combo == 1:
#                 if self.animation > 3:
#                     KeyBoardDic.update(j=False)
#                     self.combo = 0
#                 self.animation = (self.animation + 1) % 5
#                 pass
#             elif self.combo == 2:
#                 if self.animation > 7:
#                     KeyBoardDic.update(j=False)
#                     self.combo = 0
#                 self.animation = (self.animation + 1) % 9
#             else:
#                 if self.animation > 16:
#                     KeyBoardDic.update(j=False)
#                     self.combo = 0
#                 self.animation = (self.animation + 1) % 18
#
#             if self.animation == 3 or self.animation == 7 or self.animation == 12:
#                 check_attack()
#         elif self.state == 2:
#             self.animation = (self.animation + 1) % self.block
#         elif 2 < self.state < 6:
#             self.animation = (self.animation + 1) % 8
#
#     def update_state(self):
#         if KeyBoardDic['space']:
#             self.state = 0
#         elif KeyBoardDic['j']:
#             self.state = 1
#         elif KeyBoardDic['k']:
#             if KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
#                 self.state = 3
#             else:
#                 if self.animation > 5:
#                     self.animation = 0
#                 self.state = 2
#         elif KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
#             self.state = 4
#         else:
#             self.state = 5
#
#         if not self.state == 1:
#             if KeyBoardDic['w']:
#                 self.dir = 0
#             elif KeyBoardDic['s']:
#                 self.dir = 1
#             elif KeyBoardDic['a']:
#                 self.dir = 2
#             elif KeyBoardDic['d']:
#                 self.dir = 3
#
#     def update_character(self):
#         if self.state == 0:
#             self.move(1.5)
#         elif self.state == 1:
#             if self.animation == 1:
#                 self.move(2)
#             elif self.animation == 6:
#                 self.move(2)
#             elif self.animation == 10:
#                 self.move(1.5)
#             pass
#         elif self.state == 3:
#             self.move(0.5)
#             pass
#         elif self.state == 4:
#             self.move(1)
#             pass
#         else:
#             pass
#
#     def move(self, i):
#         if self.dir == 0:
#             if self.y < get_canvas_height() - 80:
#                 self.y += i
#             else:
#                 self.y = get_canvas_height() - 80
#         elif self.dir == 1:
#             if self.y > 120:
#                 self.y -= i
#             else:
#                 self.y = 120
#         elif self.dir == 2:
#             if self.x > 160:
#                 self.x -= i
#             else:
#                 self.x = 160
#         elif self.dir == 3:
#             if self.x < get_canvas_width() - 160:
#                 self.x += i
#             else:
#                 self.x = get_canvas_width() - 160
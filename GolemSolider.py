from pico2d import *
import game_framework
import random

TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_DEADSTATE = range(3)


class MoveState:
    def enter(golemsoldier, event):
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        from main_state import character
        pass

    def draw(golemsoldier):
        golemsoldier.walk.clip_draw(200 * golemsoldier.animationX, 200 * golemsoldier.animationDir,
                                    200, 200, golemsoldier.x, golemsoldier.y)
        pass


class AttackState:
    def enter(golemsoldier, event):
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        pass

    def draw(golemsoldier):
        golemsoldier.attack.clip_draw(200 * golemsoldier.animationX, 200 * golemsoldier.animationDir,
                                      200, 200, golemsoldier.x, golemsoldier.y)
        pass

class DeadState:
    def enter(golemsoldier, event):
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        pass

    def draw(golemsoldier):
        pass


next_state_table = [MoveState, AttackState, DeadState]


class golemsoldier:
    die = None
    walk = None
    attack = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationDir = 0
        self.cur_state = 0
        self.hp = 1
        self.dead = False
        self.delay = 0
        self.i = 0.2
        if golemsoldier.die == None:
            golemsoldier.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
            golemsoldier.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
            golemsoldier.die = load_image("monster/GolemSoldier/soldier_die.png")
        pass

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[event]
            self.cur_state.enter(self, event)


# from pico2d import *
# import random
#
#
# class GolemSoldier:
#     walk = None
#     attak = None
#     die = None
#
#     def __init__(self):
#         self.x = random.randint(200, get_canvas_width() - 200)
#         self.y = random.randint(200, get_canvas_height() - 100)
#         self.animationX = 0
#         self.animationDir = 0
#         self.statement = 0
#         self.hp = 1
#         self.dead = False
#         self.delay = 0
#         self.i = 0.2
#         if GolemSoldier.die == None:
#             GolemSoldier.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
#             GolemSoldier.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
#             GolemSoldier.die = load_image("monster/GolemSoldier/soldier_die.png")
#
#     def draw(self):
#         if self.dead:
#             self.die.draw(self.x, self.y)
#         else:
#             if self.statement == 0:
#                 self.walk.clip_draw(200 * self.animationX, 200 * self.animationDir, 200, 200, self.x, self.y)
#             else:
#                 self.attack.clip_draw(200 * self.animationX, 200 * self.animationDir, 200, 200, self.x, self.y)
#
#     def update_animation(self):
#         if self.statement == 0:
#             self.animationX = (self.animationX + 1) % 8
#         else:
#             self.animationX += 1
#             if self.animationX == 13:
#                 self.statement = 0
#                 self.delay = 20
#                 self.animationX = 0
#
#     def move(self, character):
#         if self.delay == 0:
#             if self.statement == 0:
#                 t = self.i / 100
#                 self.x = (1 - t) * self.x + t * character.x
#                 self.y = (1 - t) * self.y + t * character.y
#                 if self.x < character.x:
#                     dx = character.x - self.x
#                     if self.y < character.y:
#                         dy = character.y - self.y
#                         if dx < dy:
#                             self.animationDir = 0
#                         else:
#                             self.animationDir = 3
#
#                     else:
#                         dy = self.y - character.y
#                         if dx < dy:
#                             self.animationDir = 1
#                         else:
#                             self.animationDir = 3
#                 else:
#                     dx = self.x - character.x
#                     if self.y < character.y:
#                         dy = character.y - self.y
#                         if dx < dy:
#                             self.animationDir = 0
#                         else:
#                             self.animationDir = 2
#
#                     else:
#                         dy = self.y - character.y
#                         if dx < dy:
#                             self.animationDir = 1
#                         else:
#                             self.animationDir = 2
#
#                 if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
#                     self.statement = 1
#                     self.animationX = 0
#             else:
#                 pass
#         else:
#             self.delay -= 1
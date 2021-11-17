from pico2d import *
import game_framework
import game_world
import Check_Collide
import random

TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_DEADSTATE = range(3)


class MoveState:
    def enter(golemsoldier, event):
        golemsoldier.animationX = 0
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        from main_state import character
        if golemsoldier.delay == 0:
            t = golemsoldier.i / 100
            golemsoldier.x = (1 - t) * golemsoldier.x + t * character.x
            golemsoldier.y = (1 - t) * golemsoldier.y + t * character.y
            if golemsoldier.x < character.x:
                dx = character.x - golemsoldier.x
                if golemsoldier.y < character.y:
                    dy = character.y - golemsoldier.y
                    if dx < dy:
                        golemsoldier.animationDir = 0
                    else:
                        golemsoldier.animationDir = 3

                else:
                    dy = golemsoldier.y - character.y
                    if dx < dy:
                        golemsoldier.animationDir = 1
                    else:
                        golemsoldier.animationDir = 3
            else:
                dx = golemsoldier.x - character.x
                if golemsoldier.y < character.y:
                    dy = character.y - golemsoldier.y
                    if dx < dy:
                        golemsoldier.animationDir = 0
                    else:
                        golemsoldier.animationDir = 2

                else:
                    dy = golemsoldier.y - character.y
                    if dx < dy:
                        golemsoldier.animationDir = 1
                    else:
                        golemsoldier.animationDir = 2

            if (golemsoldier.x - character.x) ** 2 + (golemsoldier.y - character.y) ** 2 < 6000:
                golemsoldier.add_event(TURN_TO_ATTACKSTATE)
                golemsoldier.animationX = 0

        else:
            golemsoldier.delay -= 1

        golemsoldier.animationX = (golemsoldier.animationX +
                                   game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 8
        pass

    def draw(golemsoldier):
        golemsoldier.walk.clip_draw(200 * int(golemsoldier.animationX), 200 * golemsoldier.animationDir,
                                    200, 200, golemsoldier.x, golemsoldier.y)
        pass


class AttackState:
    def enter(golemsoldier, event):
        golemsoldier.animationX = 0
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        golemsoldier.animationX = (golemsoldier.animationX +
                                   game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if golemsoldier.animationX > 13:
            golemsoldier.add_event(TURN_TO_MOVESTATE)

        from main_state import character
        if golemsoldier.animationX > 7 and \
                Check_Collide.check_collide(golemsoldier, character) and character.powerOverwhelming < 0:
            character.hp -= 1
            character.powerOverwhelming = 2.0
            character.check_hp()
        pass

    def draw(golemsoldier):
        golemsoldier.attack.clip_draw(200 * int(golemsoldier.animationX), 200 * golemsoldier.animationDir,
                                      200, 200, golemsoldier.x, golemsoldier.y)
        draw_rectangle(*golemsoldier.get_attack_range())
        pass

class DeadState:
    def enter(golemsoldier, event):
        from main_state import cur_stage
        cur_stage.mobnum -= 1
        golemsoldier.animationX = 0
        game_world.change_layer(golemsoldier, 1, 0)
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        pass

    def draw(golemsoldier):
        golemsoldier.die.draw(golemsoldier.x, golemsoldier.y)
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
        self.event_que = []
        self.cur_state = MoveState
        self.hp = 1
        self.dead = False
        self.delay = 0
        self.i = 0.2
        if golemsoldier.die == None:
            golemsoldier.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
            golemsoldier.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
            golemsoldier.die = load_image("monster/GolemSoldier/soldier_die.png")
        pass

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def get_attack_range(self):
        if self.animationDir == 0:
            return self.x - 25, self.y, self.x + 25, self.y + 100
        elif self.animationDir == 1:
            return self.x - 25, self.y, self.x + 25, self.y - 100
        elif self.animationDir == 2:
            return self.x - 100, self.y - 25, self.x, self.y + 25
        elif self.animationDir == 3:
            return self.x, self.y - 25, self.x + 100, self.y + 25

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[event]
            self.cur_state.enter(self, event)

    def check_hp(self):
        if self.hp == 0:
            self.add_event(TURN_TO_DEADSTATE)


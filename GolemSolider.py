from pico2d import *

import Character
import game_framework
import game_world
import server
import Check_Collide
import random
import item

TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_DEADSTATE = range(3)


class MoveState:
    def enter(golemsoldier, event):
        golemsoldier.animationX = 0
        pass

    def exit(golemsoldier, event):
        pass

    def do(golemsoldier):
        if golemsoldier.delay == 0:
            t = golemsoldier.i / 100
            golemsoldier.x = (1 - t) * golemsoldier.x + t * server.character.x
            golemsoldier.y = (1 - t) * golemsoldier.y + t * server.character.y
            if golemsoldier.x < server.character.x:
                dx = server.character.x - golemsoldier.x
                if golemsoldier.y < server.character.y:
                    dy = server.character.y - golemsoldier.y
                    if dx < dy:
                        golemsoldier.animationDir = 0
                    else:
                        golemsoldier.animationDir = 3

                else:
                    dy = golemsoldier.y - server.character.y
                    if dx < dy:
                        golemsoldier.animationDir = 1
                    else:
                        golemsoldier.animationDir = 3
            else:
                dx = golemsoldier.x - server.character.x
                if golemsoldier.y < server.character.y:
                    dy = server.character.y - golemsoldier.y
                    if dx < dy:
                        golemsoldier.animationDir = 0
                    else:
                        golemsoldier.animationDir = 2

                else:
                    dy = golemsoldier.y - server.character.y
                    if dx < dy:
                        golemsoldier.animationDir = 1
                    else:
                        golemsoldier.animationDir = 2

            if (golemsoldier.x - server.character.x) ** 2 + (golemsoldier.y - server.character.y) ** 2 < 6000:
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
        golemsoldier.attacked = False
        pass

    def exit(golemsoldier, event):
        golemsoldier.played = False
        pass

    def do(golemsoldier):
        golemsoldier.animationX = (golemsoldier.animationX +
                                   game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if golemsoldier.animationX > 13:
            golemsoldier.add_event(TURN_TO_MOVESTATE)

        if 7 < golemsoldier.animationX and not golemsoldier.played:
            golemsoldier.attackSound.play()
            golemsoldier.played = True

        if 7 < golemsoldier.animationX < 10 and \
                Check_Collide.check_attack(golemsoldier, server.character) and server.character.powerOverwhelming < 0:
            if server.character.check_defense(golemsoldier):
                if golemsoldier.attacked:
                    pass
                else:
                    golemsoldier.attacked = True
                    server.character.cur_state = Character.DefenceState
                    server.character.animation = 0
                    server.character.block = 6
            else:
                server.character.hp -= 1
                server.character.powerOverwhelming = 1.0
                server.character.check_hp()
        pass

    def draw(golemsoldier):
        golemsoldier.attack.clip_draw(200 * int(golemsoldier.animationX), 200 * golemsoldier.animationDir,
                                      200, 200, golemsoldier.x, golemsoldier.y)
        pass

class DeadState:
    def enter(golemsoldier, event):
        server.dungeon.mobnum -= 1
        server.golemsoldierNum += 1
        golemsoldier.animationX = 0
        game_world.change_layer(golemsoldier, 1, 0)
        seed = random.randint(0, 100)
        if seed < 16:
            game_world.add_object(item.Item(golemsoldier.x, golemsoldier.y, item.Crystal), 0)
        elif seed < 32:
            game_world.add_object(item.Item(golemsoldier.x, golemsoldier.y, item.Core), 0)
        elif seed < 48:
            game_world.add_object(item.Item(golemsoldier.x, golemsoldier.y, item.Stone), 0)
        elif seed < 64:
            game_world.add_object(item.Item(golemsoldier.x, golemsoldier.y, item.Steel), 0)
        elif seed < 80:
            game_world.add_object(item.Item(golemsoldier.x, golemsoldier.y, item.Plastic), 0)
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
    attackSound = None
    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationDir = 0
        self.event_que = []
        self.cur_state = MoveState
        self.hp = 1

        self.attacked = False
        self.played = False
        self.dead = False
        self.delay = 0
        self.i = 0.2
        if golemsoldier.die == None:
            golemsoldier.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
            golemsoldier.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
            golemsoldier.die = load_image("monster/GolemSoldier/soldier_die.png")
            golemsoldier.attackSound = load_wav("bgm/golemsoldier_attack.wav")
            golemsoldier.attackSound.set_volume(16)
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


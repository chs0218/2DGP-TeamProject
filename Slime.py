from pico2d import *

import Character
import server
import Check_Collide
import game_framework
import game_world
import random
import item

TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_ABSORBSTATE, TURN_TO_EXPELSTATE, TURN_TO_DEADSTATE = range(5)


class MoveState:
    def enter(slime, event):
        slime.animationX = 0
        slime.animationY = 0
        pass

    def exit(slime, event):
        pass

    def do(slime):
        t = slime.i / 100
        slime.x = (1 - t) * slime.x + t * server.character.x
        slime.y = (1 - t) * slime.y + t * server.character.y
        if (slime.x - server.character.x) ** 2 + (slime.y - server.character.y) ** 2 < 3200:
            seed = random.randint(0, 3)
            if seed == 3:
                slime.add_event(TURN_TO_ABSORBSTATE)
                game_world.change_layer(slime, 1, 3)
            else:
                slime.add_event(TURN_TO_ATTACKSTATE)

        slime.animationX = (slime.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 8
        pass

    def draw(slime):
        slime.walk.clip_draw(100 * int(slime.animationX), 0, 100, 100, slime.x, slime.y)
        pass


class AttackState:
    def enter(slime, event):
        slime.attacked = False
        slime.animationX = 0
        slime.animationY = 1
        pass

    def exit(slime, event):
        pass

    def do(slime):
        slime.animationX = (slime.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)

        if slime.animationX > 8:
            if slime.animationY == 1:
                slime.animationX = 0
                slime.animationY -= 1
            else:
                slime.animationY = 1
                slime.add_event(TURN_TO_MOVESTATE)
                slime.delay = 50
        if slime.animationY == 1 and slime.animationX > 6 and \
                Check_Collide.check_attack(slime, server.character) and server.character.powerOverwhelming < 0:
            if server.character.check_defense(slime):
                if slime.attacked:
                    pass
                else:
                    slime.attacked = True
                    server.character.cur_state = Character.DefenceState
                    server.character.animation = 0
                    server.character.block = 6
            else:
                server.character.hp -= 1
                server.character.powerOverwhelming = 1.0
                server.character.check_hp()
        elif slime.animationY == 0 and slime.animationX < 3 and \
                Check_Collide.check_attack(slime, server.character) and server.character.powerOverwhelming < 0:
            if server.character.check_defense(slime):
                if slime.attacked:
                    pass
                else:
                    slime.attacked = True
                    server.character.cur_state = Character.DefenceState
                    server.character.animation = 0
                    server.character.block = 6
            else:
                server.character.hp -= 1
                server.character.powerOverwhelming = 1.0
                server.character.check_hp()
        pass

    def draw(slime):
        slime.attack.clip_draw(200 * int(slime.animationX), 200 * slime.animationY, 200, 200, slime.x, slime.y)
        draw_rectangle(*slime.get_attack_range())
        pass


class AbsorbState:
    def enter(slime, event):
        slime.animationX = 0
        slime.animationY = 1
        slime.expelnum = 0
        pass

    def exit(slime, event):
        game_world.change_layer(slime, 3, 1)
        pass

    def do(slime):
        if slime.expelnum > 10:
            slime.add_event(TURN_TO_EXPELSTATE)

        slime.x = server.character.x
        slime.y = server.character.y

        slime.animationX = (slime.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)

        if slime.animationX > 10 and slime.animationY == 1:
            slime.animationY -= 1
            slime.animationX = 0
            slime.expelCount = True

        elif slime.animationY == 0 and slime.animationX > 10:
                server.character.hp -= 1
                server.character.powerOverwhelming = 2.0
                server.character.check_hp()
        slime.animationX %= 10
        pass

    def draw(slime):
        slime.absorbed.clip_draw(100 * int(slime.animationX), 100 * slime.animationY, 100, 100, slime.x, slime.y)
        pass


class ExpelState:
    def enter(slime, event):
        slime.animationX = 0
        slime.animationY = 0
        pass

    def exit(slime, event):
        pass

    def do(slime):
        slime.animationX = (slime.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if slime.animationX > 7:
            slime.delay = 100
            slime.add_event(TURN_TO_MOVESTATE)
        pass

    def draw(slime):
        slime.expel.clip_draw(200 * int(slime.animationX), 200 * slime.animationY, 200, 200, slime.x, slime.y)
        pass


class DeadState:
    def enter(slime, event):
        server.dungeon.mobnum -= 1
        server.slimeNum += 1
        slime.animationX = 0
        slime.animationY = 0
        game_world.change_layer(slime, 1, 0)
        game_world.add_object(item.Item(slime.x, slime.y, 0), 0)
        pass

    def exit(slime, event):
        pass

    def do(slime):
        pass

    def draw(slime):
        slime.die.draw(slime.x, slime.y)
        pass


next_state_table = [MoveState, AttackState, AbsorbState, ExpelState, DeadState]


class slime:
    die = None
    walk = None
    attack = None
    absorbed = None
    expel = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationY = 0
        self.dir = random.random()*2*math.pi
        self.event_que = []
        self.cur_state = MoveState
        self.hp = 1
        self.wait_timer = 2.0
        self.dead = False
        self.expelCount = False
        self.expelnum = 0
        slime.attacked = False
        self.i = 0.2

        if slime.die == None:
            slime.die = load_image("monster/slime/slimes_die.png")
            slime.walk = load_image("monster/slime/slime_walk.png")
            slime.attack = load_image("monster/slime/slime_hit_attack.png")
            slime.absorbed = load_image("monster/slime/slimeabsorbed_attack.png")
            slime.expel = load_image("monster/slime/slime_expel.png")
        pass

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def get_attack_range(self):
        return self.x - 60, self.y - 60, self.x + 60, self.y + 60

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

    def countexpel(self):
        if self.expelCount:
            self.expelnum += 1
        pass

    def check_hp(self):
        if self.hp == 0:
            self.add_event(TURN_TO_DEADSTATE)
from pico2d import *
import Character
import game_framework
import game_world
import Check_Collide
import server
import random
import item

TURN_TO_WAKESTATE, TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_DEADSTATE = range(4)


class MoveState:
    def enter(golemkamikaze, event):
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        t = golemkamikaze.i / 100
        golemkamikaze.x = (1 - t) * golemkamikaze.x + t * server.character.x
        golemkamikaze.y = (1 - t) * golemkamikaze.y + t * server.character.y
        if (golemkamikaze.x - server.character.x) ** 2 + (golemkamikaze.y - server.character.y) ** 2 < 6000:
            golemkamikaze.add_event(TURN_TO_ATTACKSTATE)

        golemkamikaze.animationX = (golemkamikaze.animationX +
                                    game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 4
        pass

    def draw(golemkamikaze):
        golemkamikaze.walk.clip_draw(100 * int(golemkamikaze.animationX), 0,
                                     100, 100, golemkamikaze.x, golemkamikaze.y)
        pass


class AttackState:
    def enter(golemkamikaze, event):
        golemkamikaze.attacked = False
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        t = golemkamikaze.i / 20
        golemkamikaze.x = (1 - t) * golemkamikaze.x + t * server.character.x
        golemkamikaze.y = (1 - t) * golemkamikaze.y + t * server.character.y

        golemkamikaze.animationX = (golemkamikaze.animationX +
                                    game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if golemkamikaze.animationX > 10:
            if golemkamikaze.animationY == 0:
                golemkamikaze.explosion.play()
                golemkamikaze.animationY += 1
            else:
                golemkamikaze.add_event(TURN_TO_DEADSTATE)

        if golemkamikaze.animationY == 1 and \
                Check_Collide.check_attack(golemkamikaze, server.character) and server.character.powerOverwhelming < 0:
            if server.character.check_defense(golemkamikaze):
                if golemkamikaze.attacked:
                    pass
                else:
                    golemkamikaze.attacked = True
                    server.character.cur_state = Character.DefenceState
                    server.character.animation = 0
                    server.character.block = 6
            else:
                server.character.hp -= 1
                server.character.powerOverwhelming = 1.0
                server.character.check_hp()
        pass

    def draw(golemkamikaze):
        golemkamikaze.attack.clip_draw(300 * int(golemkamikaze.animationX), 300 * golemkamikaze.animationY,
                                       300, 300, golemkamikaze.x, golemkamikaze.y)
        pass


class SleepState:
    def enter(golemkamikaze, event):
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        golemkamikaze.delay = golemkamikaze.delay - game_framework.frame_time
        if golemkamikaze.delay < 0:
            golemkamikaze.add_event(TURN_TO_WAKESTATE)
        pass

    def draw(golemkamikaze):
        golemkamikaze.slept.draw(golemkamikaze.x, golemkamikaze.y)
        pass


class WakeState:
    def enter(golemkamikaze, event):
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        golemkamikaze.animationX = (golemkamikaze.animationX +
                                    game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if golemkamikaze.animationX > 4:
            golemkamikaze.add_event(TURN_TO_MOVESTATE)
        pass

    def draw(golemkamikaze):
        golemkamikaze.wake.clip_draw(100 * int(golemkamikaze.animationX), 0,
                                     100, 100, golemkamikaze.x, golemkamikaze.y)
        pass


class DeadState:
    def enter(golemkamikaze, event):
        server.dungeon.mobnum -= 1
        server.golemkamikazeNum += 1
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        game_world.change_layer(golemkamikaze, 1, 0)
        seed = random.randint(0, 100)
        if seed < 16:
            game_world.add_object(item.Item(golemkamikaze.x, golemkamikaze.y, item.Crystal), 0)
        elif seed < 32:
            game_world.add_object(item.Item(golemkamikaze.x, golemkamikaze.y, item.Core), 0)
        elif seed < 48:
            game_world.add_object(item.Item(golemkamikaze.x, golemkamikaze.y, item.Stone), 0)
        elif seed < 64:
            game_world.add_object(item.Item(golemkamikaze.x, golemkamikaze.y, item.Steel), 0)
        elif seed < 80:
            game_world.add_object(item.Item(golemkamikaze.x, golemkamikaze.y, item.Plastic), 0)
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        pass

    def draw(golemkamikaze):
        golemkamikaze.die.draw(golemkamikaze.x, golemkamikaze.y)
        pass


next_state_table = [WakeState, MoveState, AttackState, DeadState]


class golemkamikaze:
    slept = None
    wake = None
    walk = None
    attack = None
    die = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationY = 0
        self.delay = 0.5
        self.event_que = []
        golemkamikaze.attacked = False
        self.cur_state = SleepState
        self.i = 0.2
        self.explosion = load_wav("bgm/explosion.wav")
        self.explosion.set_volume(16)

        if golemkamikaze.die == None:
            golemkamikaze.slept = load_image("monster/golemkamikaze/golemkamikaze_idleslept.png")
            golemkamikaze.wake = load_image("monster/golemkamikaze/golemkamikaze_wake.png")
            golemkamikaze.walk = load_image("monster/golemkamikaze/golemkamikaze_walk.png")
            golemkamikaze.attack = load_image("monster/golemkamikaze/golemkamikaze_attack.png")
            golemkamikaze.die = load_image("monster/golemkamikaze/kamikaze_die.png")

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def get_attack_range(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

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
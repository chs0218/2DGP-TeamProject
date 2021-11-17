from pico2d import *
import game_framework
import game_world
import Check_Collide
import random

TURN_TO_WAKESTATE, TURN_TO_MOVESTATE, TURN_TO_ATTACKSTATE, TURN_TO_DEADSTATE = range(4)


class MoveState:
    def enter(golemkamikaze, event):
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        from main_state import character
        t = golemkamikaze.i / 100
        golemkamikaze.x = (1 - t) * golemkamikaze.x + t * character.x
        golemkamikaze.y = (1 - t) * golemkamikaze.y + t * character.y
        if (golemkamikaze.x - character.x) ** 2 + (golemkamikaze.y - character.y) ** 2 < 6000:
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
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        golemkamikaze.animationX = (golemkamikaze.animationX +
                                    game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time)
        if golemkamikaze.animationX > 10:
            if golemkamikaze.animationY == 0:
                golemkamikaze.animationY += 1
            else:
                golemkamikaze.add_event(TURN_TO_DEADSTATE)

        from main_state import character
        if golemkamikaze.animationY == 1 and \
                Check_Collide.check_collide(golemkamikaze, character) and character.powerOverwhelming < 0:
            character.hp -= 1
            character.powerOverwhelming = 2.0
            character.check_hp()
        pass

    def draw(golemkamikaze):
        golemkamikaze.attack.clip_draw(300 * int(golemkamikaze.animationX), 300 * golemkamikaze.animationY,
                                       300, 300, golemkamikaze.x, golemkamikaze.y)
        draw_rectangle(*golemkamikaze.get_attack_range())
        pass


class SleepState:
    def enter(golemkamikaze, event):
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(golemkamikaze, event):
        pass

    def do(golemkamikaze):
        from main_state import character
        if (golemkamikaze.x - character.x) ** 2 + (golemkamikaze.y - character.y) ** 2 < 6000:
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
        from main_state import cur_stage
        cur_stage.mobnum -= 1
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        game_world.change_layer(golemkamikaze, 1, 0)
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
        self.event_que = []
        self.cur_state = SleepState
        self.i = 0.2
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
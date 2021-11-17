from pico2d import *
import game_framework
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
        golemkamikaze.animationX = 0
        golemkamikaze.animationY = 0
        pass

    def exit(slime, event):
        pass

    def do(slime):
        pass

    def draw(slime):
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
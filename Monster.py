from pico2d import *
import random

class monster:
    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animation = 0
        self.event_que = []
        pass

    def draw(self):
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def updateState(self):
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.updateState()
            self.animation = 0
            self.cur_state.enter(self, event)

    def move(self, character):
        pass
import time
frame_time = 0.0
FRAMES_PER_TIME = 16
MONSTER_FRAMES_PER_TIME = 12
DOOR_FRAMES_PER_TIME = 6

class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


playing = None
stack = None


def change_state(state):
    global stack
    if len(stack) > 0:
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()
    stack.append(state)
    state.enter()


def push_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(state)
    state.enter()


def pop_state():
    global stack
    if len(stack) > 0:
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if len(stack) > 0:
        stack[-1].resume()


def quit():
    global playing
    playing = False


def play(start_state):
    global playing, stack, frame_time
    playing = True
    stack = [start_state]
    start_state.enter()

    current_time = time.time()
    while playing:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        # frame_rate = 1.0 / frame_time
        current_time += frame_time
        # print("Frame Time: %f sec, Frame Rate: %f fps" % (frame_time, frame_rate))
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()


def game_framework():
    start_state = GameState('StartState')
    play(start_state)


if __name__ == '__main__':
    game_framework()
import game_framework
import main_state
import server
from pico2d import *
import server

class Stage:
    def __init__(self):
        self.normal = load_image("map/Stage_Normal.png")
        self.hard = load_image("map/Stage_Hard.png")
        self.veryhard = load_image("map/Stage_VeryHard.png")
    def draw(self):
        if server.difficulty == 0:
            self.normal.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        elif server.difficulty == 1:
            self.hard.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        else:
            self.veryhard.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    pass


name = "TitleState"
stage = None
Width, Height = 1276, 720

def enter():
    global stage
    stage = Stage()
    pass


def exit():
    global stage
    del stage
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                server.difficulty = (server.difficulty - 1) % 3
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                server.difficulty = (server.difficulty + 1) % 3
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(main_state)
    pass


def draw():
    clear_canvas()
    stage.draw()
    update_canvas()
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass







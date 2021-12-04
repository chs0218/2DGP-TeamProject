import game_framework
import game_world
import title_state
import server
from pico2d import *

image = None
bkimage = None
bkimage2 = None
font = None
name = "ResultState"


class slime:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animationX = 0
        if slime.image == None:
            slime .image = load_image("monster/slime/slime_walk.png")

    def draw(self):
        slime.image.clip_draw(100 * int(self.animationX), 0, 100, 100, self.x, self.y)

    def update(self):
        self.animationX = (self.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 8

class golemsoldier:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animationX = 0
        if golemsoldier.image == None:
            golemsoldier.image = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")

    def draw(self):
        golemsoldier.image.clip_draw(200 * int(self.animationX), 200, 200, 200, self.x, self.y, 150, 150)

    def update(self):
        self.animationX = (self.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 8


class golemkamikaze:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animationX = 0
        if golemkamikaze.image == None:
            golemkamikaze.image = load_image("monster/golemkamikaze/golemkamikaze_walk.png")

    def draw(self):
        golemkamikaze.image.clip_draw(100 * int(self.animationX), 0, 100, 100, self.x, self.y)

    def update(self):
        self.animationX = (self.animationX + game_framework.MONSTER_FRAMES_PER_TIME * game_framework.frame_time) % 4


def enter():
    global image, bkimage, bkimage2, font, score

    globalX = get_canvas_width() // 2 - 100
    globalY = get_canvas_height() // 2 + 45

    image = load_image("result/result.png")
    bkimage = load_image("result/bkground.png")
    bkimage2 = load_image("result/bkground2.png")
    font = load_font('Youth.ttf', 20)

    Slime = [slime(globalX + (_ * 10), globalY) for _ in range(server.slimeNum)]
    Golemsolider = [golemsoldier(globalX + (_ * 10), globalY - 50) for _ in range(server.golemsoldierNum)]
    Golemkamikaze = [golemkamikaze(globalX + (_ * 10), globalY - 100) for _ in range(server.golemkamikazeNum)]
    game_world.add_objects(Slime, 1)
    game_world.add_objects(Golemsolider, 1)
    game_world.add_objects(Golemkamikaze, 1)

    server.score = 500 * server.slimeNum + 1000 * server.golemsoldierNum + 800 * server.golemkamikazeNum
    pass


def exit():

    game_world.clear()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(title_state)
    pass


def draw():
    clear_canvas()
    bkimage.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    bkimage2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    for game_object in game_world.all_objects():
        game_object.draw()
    font.draw(170, 600, '쓰러트린 슬라임 수: %d' % server.slimeNum, (0, 0, 0))
    font.draw(170, 570, '쓰러트린 골렘전사 수: %d' % server.golemsoldierNum, (0, 0, 0))
    font.draw(170, 540, '쓰러트린 자폭로봇 수: %d' % server.golemkamikazeNum, (0, 0, 0))
    font.draw(170, 510, '점수: %d' % server.score, (0, 0, 0))
    update_canvas()
    handle_events()
    pass


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    pass


def pause():
    pass


def resume():
    pass







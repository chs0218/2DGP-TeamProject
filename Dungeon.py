from pico2d import *

class dungeon:
    BK = None
    BK2 = None
    Door = None
    def __init__(self):
        if dungeon.BK == None:
            dungeon.BK = load_image("map/Dungeon_BK.png")
            dungeon.BK2 = load_image("map/BKWalls.png")
            dungeon.Door = load_image("map/Door.png")
        self.DoorAnimation = 0
        self.isClear = False

    def draw(self):
        dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        dungeon.Door.clip_draw(200 * self.DoorAnimation, 0, 200, 200, get_canvas_width() // 2, get_canvas_height() - 60)
from pico2d import *
import game_framework

class dungeon:
    BK = None
    BK2 = None
    Door = None
    def __init__(self, n):
        if dungeon.BK == None:
            dungeon.BK = load_image("map/Dungeon_BK.png")
            dungeon.BK2 = load_image("map/BKWalls.png")
            dungeon.Door = load_image("map/Door.png")
        self.DoorAnimation = 0
        self.mobnum = n
        self.isClear = False

    def get_bb(self):
        return get_canvas_width() // 2 - 25, get_canvas_height() - 115, \
               get_canvas_width() // 2 + 25, get_canvas_height() - 65

    def update(self):
        if self.mobnum == 0:
            self.isClear = True
            self.mobnum -= 1
        if self.isClear and self.DoorAnimation < 11:
            self.DoorAnimation = (self.DoorAnimation +
                                  game_framework.DOOR_FRAMES_PER_TIME * game_framework.frame_time)
        elif self.DoorAnimation < 7:
            self.DoorAnimation = (self.DoorAnimation + game_framework.DOOR_FRAMES_PER_TIME
                                  * game_framework.frame_time)
        pass

    def draw(self):
        dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        dungeon.Door.clip_draw(200 * int(self.DoorAnimation), 0, 200, 200, get_canvas_width() // 2, get_canvas_height() - 60)
        draw_rectangle(*self.get_bb())
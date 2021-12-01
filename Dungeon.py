from pico2d import *
import server
import Slime
import GolemSolider
import Golemkamikaze
import game_world
import Check_Collide
import game_framework
import result_state
import math

import server

class Stage1:
    def enter(Dungeon):
        Dungeon.mobnum = 10
        Dungeon.isClear = False
        Dungeon.DoorAnimation = 0
        server.slime = [Slime.slime() for _ in range(10)]
        game_world.add_objects(server.slime, 1)
        pass

    def exit(Dungeon):
        for slime in server.slime:
            game_world.remove_object(slime)
        server.slime = []
        pass

    def draw(Dungeon):
        Dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.Door.clip_draw(200 * int(Dungeon.DoorAnimation), 0, 200, 200,
                               get_canvas_width() // 2, get_canvas_height() - 60)
        draw_rectangle(*Dungeon.get_bb())

    def do(Dungeon):
        pass

class Stage2:
    def enter(Dungeon):
        Dungeon.mobnum = 10
        Dungeon.isClear = False
        Dungeon.DoorAnimation = 0
        server.character.x = 630
        server.character.y = 120
        server.golemsoldier = [GolemSolider.golemsoldier() for _ in range(10)]
        game_world.add_objects(server.golemsoldier, 1)
        pass

    def exit(Dungeon):
        for golemsoldier in server.golemsoldier:
            game_world.remove_object(golemsoldier)
        server.golemsoldier = []
        pass

    def draw(Dungeon):
        Dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.Door.clip_draw(200 * int(Dungeon.DoorAnimation), 0, 200, 200,
                               get_canvas_width() // 2, get_canvas_height() - 60)
        Dungeon.Door.clip_composite_draw(int(Dungeon.DoorAnimation) * 200, 0, 200, 200,
                                         math.radians(180), 'h', get_canvas_width() // 2, 60, 200, 200)
        draw_rectangle(*Dungeon.get_bb())

    def do(Dungeon):
        pass

class Stage3:
    def enter(Dungeon):
        Dungeon.mobnum = 5
        Dungeon.isClear = False
        Dungeon.DoorAnimation = 0
        server.character.x = 630
        server.character.y = 120
        server.golemkamikaze = [Golemkamikaze.golemkamikaze() for _ in range(5)]
        game_world.add_objects(server.golemkamikaze, 1)
        pass

    def exit(Dungeon):
        for golemkamikaze in server.golemkamikaze:
            game_world.remove_object(golemkamikaze)
        server.golemkamikaze = []
        pass

    def draw(Dungeon):
        Dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.Door.clip_draw(200 * int(Dungeon.DoorAnimation), 0, 200, 200,
                               get_canvas_width() // 2, get_canvas_height() - 60)
        Dungeon.Door.clip_composite_draw(int(Dungeon.DoorAnimation) * 200, 0, 200, 200,
                                         math.radians(180), 'h', get_canvas_width() // 2, 60, 200, 200)
        draw_rectangle(*Dungeon.get_bb())

    def do(Dungeon):
        pass


class Stage4:
    def enter(Dungeon):
        Dungeon.mobnum = 15
        Dungeon.isClear = False
        Dungeon.DoorAnimation = 0
        server.character.x = 630
        server.character.y = 120
        server.slime = [Slime.slime() for _ in range(5)]
        server.golemsoldier = [GolemSolider.golemsoldier() for _ in range(5)]
        server.golemkamikaze = [Golemkamikaze.golemkamikaze() for _ in range(5)]
        game_world.add_objects(server.slime, 1)
        game_world.add_objects(server.golemsoldier, 1)
        game_world.add_objects(server.golemkamikaze, 1)
        pass

    def exit(Dungeon):
        pass

    def draw(Dungeon):
        Dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.Door.clip_draw(200 * int(Dungeon.DoorAnimation), 0, 200, 200,
                               get_canvas_width() // 2, get_canvas_height() - 60)
        Dungeon.Door.clip_composite_draw(int(Dungeon.DoorAnimation) * 200, 0, 200, 200,
                                         math.radians(180), 'h', get_canvas_width() // 2, 60, 200, 200)
        draw_rectangle(*Dungeon.get_bb())

    def do(Dungeon):
        pass

class WaitResult:
    def enter(Dungeon):
        pass

    def exit(Dungeon):
        for slime in server.slime:
            game_world.remove_object(slime)
        for golemsoldier in server.golemsoldier:
            game_world.remove_object(golemsoldier)
        for golemkamikaze in server.golemkamikaze:
            game_world.remove_object(golemkamikaze)
        server.slime = []
        server.golemsoldier = []
        server.golemkamikaze = []
        pass

    def draw(Dungeon):
        Dungeon.BK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.BK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        Dungeon.Door.clip_composite_draw(int(Dungeon.DoorAnimation) * 200, 0, 200, 200,
                                         math.radians(180), 'h', get_canvas_width() // 2, 60, 200, 200)
        draw_rectangle(*Dungeon.get_bb())

    def do(Dungeon):
        Dungeon.delay -= game_framework.frame_time
        if Dungeon.delay < 0:
            game_framework.change_state(result_state)
        print(Dungeon.delay)
        pass

next_stage = {
    Stage1: Stage2,
    Stage2: Stage3,
    Stage3: Stage4,
    Stage4: WaitResult,
    WaitResult: WaitResult
}


class Dungeon:
    BK = None
    BK2 = None
    Door = None
    def __init__(self):
        if Dungeon.BK == None:
            Dungeon.BK = load_image("map/Dungeon_BK.png")
            Dungeon.BK2 = load_image("map/BKWalls.png")
            Dungeon.Door = load_image("map/Door.png")
        self.DoorAnimation = 0
        self.mobnum = 0
        self.isClear = False
        self.delay = 2
        self.cur_stage = Stage1
        self.cur_stage.enter(self)

    def get_bb(self):
        return get_canvas_width() // 2 - 25, get_canvas_height() - 115, \
               get_canvas_width() // 2 + 25, get_canvas_height() - 65

    def update(self):
        if self.mobnum == 0:
            self.isClear = True
            self.mobnum -= 1
            if self.cur_stage == Stage4:
                self.ChangeStage()

        if self.isClear and self.DoorAnimation < 11:
            self.DoorAnimation = (self.DoorAnimation +
                                  game_framework.DOOR_FRAMES_PER_TIME * game_framework.frame_time)
        elif self.isClear and self.DoorAnimation >= 11:
            if Check_Collide.check_clear(self, server.character):
                self.ChangeStage()

        elif self.DoorAnimation < 7:
            self.DoorAnimation = (self.DoorAnimation + game_framework.DOOR_FRAMES_PER_TIME
                                  * game_framework.frame_time)
        self.cur_stage.do(self)
        pass

    def ChangeStage(self):
        self.cur_stage.exit(self)
        self.cur_stage = next_stage[self.cur_stage]
        self.cur_stage.enter(self)
        pass

    def draw(self):
        self.cur_stage.draw(self)
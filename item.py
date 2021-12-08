from pico2d import *

import game_framework
import game_world
import server
import Check_Collide

Potion, Crystal, Core, Plastic, Steel, Stone = range(6)
size = 50

class Item:
    crystal = None
    core = None
    plastic = None
    potion = None
    steel = None
    stone = None

    def __init__(self, x = 0, y = 0, state = 0):
        if Item.crystal == None:
            Item.crystal = load_image("inventory/item_crystalized_energy.png")
            Item.core = load_image("inventory/item_golem_core.png")
            Item.plastic = load_image("inventory/item_PlasticFilm.png")
            Item.potion = load_image("inventory/item_Potion.png")
            Item.steel = load_image("inventory/item_reinforced_steel.png")
            Item.stone = load_image("inventory/item_white_stone.png")
        self.state = state
        self.x = x
        self.y = y
        self.i = 0.4
        self.delay = 1.0
        pass

    def get_bb(self):
        return self.x - size/2, self.y - size/2, self.x + size/2, self.y + size/2

    def update(self):
        if self.delay < 0:
            t = self.i / 100
            self.x = (1 - t) * self.x + t * server.character.x
            self.y = (1 - t) * self.y + t * server.character.y
            if Check_Collide.check_clear(self, server.character):
                server.inventory.getItem(self.state)
                game_world.remove_object(self)
        else:
            self.delay -= game_framework.frame_time

    def draw(self):
        if self.state == Crystal:
            Item.crystal.draw(self.x, self.y, size, size)
        elif self.state == Core:
            Item.core.draw(self.x, self.y, size, size)
        elif self.state == Plastic:
            Item.plastic.draw(self.x, self.y, size, size)
        elif self.state == Potion:
            Item.potion.draw(self.x, self.y, size, size)
        elif self.state == Steel:
            Item.steel.draw(self.x, self.y, size, size)
        elif self.state == Stone:
            Item.stone.draw(self.x, self.y, size, size)

    def do(self):
        pass

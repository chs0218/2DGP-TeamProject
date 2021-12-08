from pico2d import *

class Inventory:
    def __init__(self):
        self.background = load_image("inventory/inventory_BG.png")
        pass

    def draw(self):
        self.background.draw(400, 400, 482, 544)
        pass
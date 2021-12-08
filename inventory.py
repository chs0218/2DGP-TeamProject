from pico2d import *
from item import *

size = 80
startX = 283
startY = 565
correctX = 21
correctY = 25
gapX = 72
gapY = 85

class Inventory:
    def __init__(self):
        self.background = load_image("inventory/inventory_BG.png")
        self.numPotion = 0
        self.numCrystal = 0
        self.numCore = 0
        self.numPlastic = 0
        self.numSteel = 0
        self.numStone = 0
        self.getitem = load_wav("bgm/getitem.wav")
        self.getitem.set_volume(8)
        items = Item()
        self.font = load_font('Youth.ttf', 20)
        del items

    def getItem(self, item):
        if item == Potion:
            self.numPotion += 1
        elif item == Crystal:
            self.numCrystal += 1
        elif item == Core:
            self.numCore += 1
        elif item == Plastic:
            self.numPlastic += 1
        elif item == Steel:
            self.numSteel += 1
        elif item == Stone:
            self.numStone += 1
        self.getitem.play()

    def draw(self, cx = 0, cy = 0):
        self.background.draw(400 + cx, 400 - cy, 482, 544)
        x = 0
        y = 0
        if self.numPotion > 0:
            Item.potion.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numPotion, (0, 0, 0))
            x += 1
        if self.numCrystal > 0:
            Item.crystal.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numCrystal, (0, 0, 0))
            x += 1
        if self.numCore > 0:
            Item.core.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numCore, (0, 0, 0))
            x += 1
        if self.numPlastic > 0:
            Item.plastic.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numPlastic, (0, 0, 0))
            x += 1
            if x > 4:
                x = 0
                y += 1
        if self.numSteel > 0:
            Item.steel.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numSteel, (0, 0, 0))
            x += 1
            if x > 4:
                x = 0
                y += 1
        if self.numStone > 0:
            Item.stone.draw(startX + cx + x * gapX, startY - cy - y * gapY, size, size)
            self.font.draw(startX + cx + x * gapX + correctX, startY - cy - y * gapY - correctY, '%d' % self.numStone, (0, 0, 0))
            if x > 4:
                x = 0
                y += 1
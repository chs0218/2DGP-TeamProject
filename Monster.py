from pico2d import *
import random

class Slime:
    die = None
    walk = None
    attack = None
    absorbed = None
    expel = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationY = 0
        self.statement = 0
        self.hp = 1
        self.delay = 0
        self.dead = False
        self.expelCount = False
        self.expelnum = 0
        self.i = 0.2
        if Slime.die == None:
            Slime.die = load_image("monster/slime/slimes_die.png")
            Slime.walk = load_image("monster/slime/slime_walk.png")
            Slime.attack = load_image("monster/slime/slime_hit_attack.png")
            Slime.absorbed = load_image("monster/slime/slimeabsorbed_attack.png")
            Slime.expel = load_image("monster/slime/slime_expel.png")

    def draw(self):
        if self.dead:
            self.die.draw(self.x, self.y)
        else:
            if self.statement == 0:
                self.walk.clip_draw(100 * self.animationX, 0, 100, 100, self.x, self.y)
            elif self.statement < 4:
                self.attack.clip_draw(200 * self.animationX, 200 * self.animationY, 200, 200, self.x, self.y)
            elif self.statement == 4:
                self.absorbed.clip_draw(100 * self.animationX, 100 * self.animationY, 100, 100, self.x, self.y)
            elif self.statement == 5:
                self.expel.clip_draw(200 * self.animationX, 200 * self.animationY, 200, 200, self.x, self.y)

    def update_animation(self):
        if self.statement == 0:
            self.animationX = (self.animationX + 1) % 8
        elif self.statement < 4:
            if self.animationX == 7:
                if self.animationY == 1:
                    self.animationY -= 1
                else:
                    self.animationY = 1
                    self.statement = 0
                    self.delay = 50
            self.animationX = (self.animationX + 1) % 8
        elif self.statement == 4:
            if self.animationX == 9 and self.animationY == 1:
                self.animationY -= 1
                self.expelCount = True
                self.animationX = 0
            self.animationX = (self.animationX + 1) % 10
        elif self.statement == 5:
            self.animationX += 1
            if self.animationX == 7:
                self.animationX = 0
                self.statement = 0
                self.delay = 100

    def move(self, character):
        if self.delay == 0:
            if self.statement == 0:
                t = self.i / 100
                self.x = (1 - t) * self.x + t * character.x
                self.y = (1 - t) * self.y + t * character.y
                if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 3200:
                    self.statement = random.randint(1, 4)
                    self.animationX = 0
                    self.expelnum = 0
                    self.animationY = 1
            elif self.statement == 4:
                self.x = character.x
                self.y = character.y
                if self.expelnum > 10:
                    self.statement = 5
                    self.animationX = 0
                    self.animationY = 0
            else:
                pass
        else:
            self.delay -= 1

    def countexpel(self):
        if self.expelCount:
            self.expelnum += 1
        pass


class GolemSoldier:
    walk = None
    attak = None
    die = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationDir = 0
        self.statement = 0
        self.hp = 1
        self.dead = False
        self.delay = 0
        self.i = 0.2
        if GolemSoldier.die == None:
            GolemSoldier.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
            GolemSoldier.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
            GolemSoldier.die = load_image("monster/GolemSoldier/soldier_die.png")

    def draw(self):
        if self.dead:
            self.die.draw(self.x, self.y)
        else:
            if self.statement == 0:
                self.walk.clip_draw(200 * self.animationX, 200 * self.animationDir, 200, 200, self.x, self.y)
            else:
                self.attack.clip_draw(200 * self.animationX, 200 * self.animationDir, 200, 200, self.x, self.y)

    def update_animation(self):
        if self.statement == 0:
            self.animationX = (self.animationX + 1) % 8
        else:
            self.animationX += 1
            if self.animationX == 13:
                self.statement = 0
                self.delay = 20
                self.animationX = 0

    def move(self, character):
        if self.delay == 0:
            if self.statement == 0:
                t = self.i / 100
                self.x = (1 - t) * self.x + t * character.x
                self.y = (1 - t) * self.y + t * character.y
                if self.x < character.x:
                    dx = character.x - self.x
                    if self.y < character.y:
                        dy = character.y - self.y
                        if dx < dy:
                            self.animationDir = 0
                        else:
                            self.animationDir = 3

                    else:
                        dy = self.y - character.y
                        if dx < dy:
                            self.animationDir = 1
                        else:
                            self.animationDir = 3
                else:
                    dx = self.x - character.x
                    if self.y < character.y:
                        dy = character.y - self.y
                        if dx < dy:
                            self.animationDir = 0
                        else:
                            self.animationDir = 2

                    else:
                        dy = self.y - character.y
                        if dx < dy:
                            self.animationDir = 1
                        else:
                            self.animationDir = 2

                if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
                    self.statement = 1
                    self.animationX = 0
            else:
                pass
        else:
            self.delay -= 1


class Golemkamikaze:
    slept = None
    wake = None
    walk = None
    attack = None
    die = None

    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationY = 0
        self.statement = 0
        self.bomb = False
        self.i = 0.2
        if Golemkamikaze.die == None:
            Golemkamikaze.slept = load_image("monster/golemkamikaze/golemkamikaze_idleslept.png")
            Golemkamikaze.wake = load_image("monster/golemkamikaze/golemkamikaze_wake.png")
            Golemkamikaze.walk = load_image("monster/golemkamikaze/golemkamikaze_walk.png")
            Golemkamikaze.attack = load_image("monster/golemkamikaze/golemkamikaze_attack.png")
            Golemkamikaze.die = load_image("monster/golemkamikaze/kamikaze_die.png")

    def draw(self):
        if self.bomb:
            self.die.draw(self.x, self.y)
        else:
            if self.statement == 0:
                self.slept.draw(self.x, self.y)
            elif self.statement == 1:
                self.wake.clip_draw(100 * self.animationX, 0, 100, 100, self.x, self.y)
            elif self.statement == 2:
                self.walk.clip_draw(100 * self.animationX, 0, 100, 100, self.x, self.y)
            else:
                self.attack.clip_draw(300 * self.animationX, 300 * self.animationY, 300, 300, self.x, self.y)

    def update_animation(self):
        if self.statement == 0:
            pass

        elif self.statement == 1:
            self.animationX += 1
            if self.animationX == 4:
                self.statement = 2
                self.animationX = 0

        elif self.statement == 2:
            self.animationX = (self.animationX + 1) % 4

        else:
            self.animationX += 1
            if self.animationX == 10:
                if self.animationY == 0:
                    self.animationY += 1
                else:
                    self.bomb = True
                    self.animationX = 0
                    self.animationY = 0
                self.animationX = 0

    def move(self, character):
        if self.statement == 0:
            if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
                self.statement = 1

        elif self.statement == 2:
            t = self.i / 100
            self.x = (1 - t) * self.x + t * character.x
            self.y = (1 - t) * self.y + t * character.y

            if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
                self.statement = 3
                self.animationX = 0
            pass
        else:
            pass
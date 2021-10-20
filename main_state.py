from pico2d import *
import random
import game_framework
import title_state

KeyBoardDic = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'j': False, 'k': False}

difficulty = None
character = None
slime = None
golemsoldier = None
golemkamikaze = None
IsClear = False
DungeonBK = None
DungeonBK2 = None
DungeonDoor = None
DoorAnimation = 0
AnimationClock = 0
SlimeNum = 0


class Character:
    def __init__(self):
        self.x = 630
        self.y = 120
        self.combo = 0
        self.state = 8
        self.block = 1
        self.Roll = load_image("player/player_roll.png")
        self.Die = load_image("player/Player_Die.png")
        self.Idle = load_image("player/player_idle.png")
        self.Walk = load_image("player/player_walk.png")
        self.Attack = load_image("player/player_attack.png")
        self.Shield = load_image("player/player_shield_defense.png")
        self.ShieldMove = load_image("player/player_shield_walk.png")
        self.animation = 0
        self.dir = 0

    def draw(self):
        if self.state == 0:
            self.Roll.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 1:
            if self.dir > 1:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y - 15)
            else:
                self.Attack.clip_draw(400 * self.animation, 400 * self.dir, 400, 400, self.x, self.y)
        elif self.state == 2:
            self.Shield.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 3:
            self.ShieldMove.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        elif self.state == 4:
            self.Walk.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)
        else:
            self.Idle.clip_draw(100 * self.animation, 100 * self.dir, 100, 100, self.x, self.y)

    def update_animation(self):
        if self.state == 0:
            if self.animation == 7:
                KeyBoardDic.update(space=False)
            self.animation = (self.animation + 1) % 8
        elif self.state == 1:
            if self.combo == 1:
                if self.animation > 3:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 5
                pass
            elif self.combo == 2:
                if self.animation > 7:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 9
            else:
                if self.animation > 16:
                    KeyBoardDic.update(j=False)
                    self.combo = 0
                self.animation = (self.animation + 1) % 18

            if self.animation == 3 or self.animation == 7 or self.animation == 12:
                check_attack()
        elif self.state == 2:
            self.animation = (self.animation + 1) % self.block
        elif 2 < self.state < 6:
            self.animation = (self.animation + 1) % 8

    def update_state(self):
        if KeyBoardDic['space']:
            self.state = 0
        elif KeyBoardDic['j']:
            self.state = 1
        elif KeyBoardDic['k']:
            if KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
                self.state = 3
            else:
                if self.animation > 5:
                    self.animation = 0
                self.state = 2
        elif KeyBoardDic['w'] or KeyBoardDic['s'] or KeyBoardDic['a'] or KeyBoardDic['d']:
            self.state = 4
        else:
            self.state = 5

        if not self.state == 1:
            if KeyBoardDic['w']:
                self.dir = 0
            elif KeyBoardDic['s']:
                self.dir = 1
            elif KeyBoardDic['a']:
                self.dir = 2
            elif KeyBoardDic['d']:
                self.dir = 3

    def update_character(self):
        if self.state == 0:
            self.move(1.5)
        elif self.state == 1:
            if self.animation == 1:
                self.move(2)
            elif self.animation == 6:
                self.move(2)
            elif self.animation == 10:
                self.move(1.5)
            pass
        elif self.state == 3:
            self.move(0.5)
            pass
        elif self.state == 4:
            self.move(1)
            pass
        else:
            pass

    def move(self, i):
        if self.dir == 0:
            if self.y < get_canvas_height() - 80:
                self.y += i
            else:
                self.y = get_canvas_height() - 80
        elif self.dir == 1:
            if self.y > 120:
                self.y -= i
            else:
                self.y = 120
        elif self.dir == 2:
            if self.x > 160:
                self.x -= i
            else:
                self.x = 160
        elif self.dir == 3:
            if self.x < get_canvas_width() - 160:
                self.x += i
            else:
                self.x = get_canvas_width() - 160


class Slime:
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
        self.die = load_image("monster/slime/slimes_die.png")
        self.walk = load_image("monster/slime/slime_walk.png")
        self.attack = load_image("monster/slime/slime_hit_attack.png")
        self.absorbed = load_image("monster/slime/slimeabsorbed_attack.png")
        self.expel = load_image("monster/slime/slime_expel.png")

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

    def move(self):
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
        self.walk = load_image("monster/GolemSoldier/GolemSoldier_Floating.png")
        self.attack = load_image("monster/GolemSoldier/GolemSoldier_Attack.png")
        self.die = load_image("monster/GolemSoldier/soldier_die.png")

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

    def move(self):
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
    def __init__(self):
        self.x = random.randint(200, get_canvas_width() - 200)
        self.y = random.randint(200, get_canvas_height() - 100)
        self.animationX = 0
        self.animationY = 0
        self.statement = 0
        self.bomb = False
        self.i = 0.2

        self.slept = load_image("monster/golemkamikaze/golemkamikaze_idleslept.png")
        self.wake = load_image("monster/golemkamikaze/golemkamikaze_wake.png")
        self.walk = load_image("monster/golemkamikaze/golemkamikaze_walk.png")
        self.attack = load_image("monster/golemkamikaze/golemkamikaze_attack.png")
        self.die = load_image("monster/golemkamikaze/kamikaze_die.png")

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

    def move(self):
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


def check_attack():
    LeftX = character.x - 50
    LeftY = character.y - 50
    RightX = character.x + 50
    RightY = character.y + 50

    if character.dir == 0:
        pass
    elif character.dir == 1:
        pass
    elif character.dir == 2:
        pass
    else:
        pass

    for i in range(SlimeNum):
        if LeftX < slime[i].x < RightX and LeftY < slime[i].y < RightY:
            slime[i].hp -= 1
            if slime[i].hp == 0:
                slime[i].dead = True
    if LeftX < golemsoldier.x < RightX and LeftY < golemsoldier.y < RightY:
        golemsoldier.hp -= 1
        if golemsoldier.hp == 0:
            golemsoldier.dead = True

def check_slime():
    for i in range(SlimeNum):
        slime[i].countexpel()
    pass


def handle_events():
    global IsClear, KeyBoardDic, character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_w:
                check_slime()
                KeyBoardDic.update(w=True)
            elif event.key == SDLK_s:
                check_slime()
                KeyBoardDic.update(s=True)
            elif event.key == SDLK_a:
                check_slime()
                KeyBoardDic.update(a=True)
            elif event.key == SDLK_d:
                check_slime()
                KeyBoardDic.update(d=True)
            elif event.key == SDLK_SPACE:
                check_slime()
                if not character.state == 0:
                    character.animation = 0
                KeyBoardDic.update(space=True)
                KeyBoardDic.update(j=False)
                character.combo = 0
            elif event.key == SDLK_j:
                if not character.state == 0 and not character.state == 1:
                    character.animation = 0
                character.combo += 1
                KeyBoardDic.update(j=True)
            elif event.key == SDLK_k:
                if not character.state == 1:
                    character.animation = 0
                KeyBoardDic.update(k=True)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_k:
                KeyBoardDic.update(k=False)
            elif event.key == SDLK_w:
                KeyBoardDic.update(w=False)
            elif event.key == SDLK_s:
                KeyBoardDic.update(s=False)
            elif event.key == SDLK_a:
                KeyBoardDic.update(a=False)
            elif event.key == SDLK_d:
                KeyBoardDic.update(d=False)

    pass


def enter():
    global character, slime, DungeonBK, DungeonBK2, DungeonDoor, difficulty, SlimeNum, golemsoldier
    global golemkamikaze
    difficulty = title_state.difficulty
    SlimeNum = 10
    character = Character()
    slime = [Slime() for i in range(SlimeNum)]
    golemsoldier = GolemSoldier()
    golemkamikaze = Golemkamikaze()
    DungeonBK = load_image("map/Dungeon_BK.png")
    DungeonBK2 = load_image("map/BKWalls.png")
    DungeonDoor = load_image("map/Door.png")
    pass


def exit():
    global character, DungeonBK, DungeonBK2, DungeonDoor, slime, golemsoldier, golemkamikaze
    del character, DungeonBK, DungeonBK2, DungeonDoor, slime, golemsoldier, golemkamikaze
    pass


def update():
    global AnimationClock
    global character, slime, golemsoldier, golemkamikaze
    if AnimationClock % 20 == 0:
        character.update_animation()
        for i in range(SlimeNum):
            if not slime[i].dead:
                slime[i].update_animation()
        if not golemsoldier.dead:
            golemsoldier.update_animation()
        if not golemkamikaze.bomb:
            golemkamikaze.update_animation()

    character.update_state()
    character.update_character()
    for i in range(SlimeNum):
        if not slime[i].dead:
            slime[i].move()
    if not golemsoldier.dead:
        golemsoldier.move()
    if not golemkamikaze.bomb:
        golemkamikaze.move()
    AnimationClock = (AnimationClock + 1) % 100


def draw():
    clear_canvas()
    DungeonBK.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    DungeonBK2.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    DungeonDoor.clip_draw(200 * DoorAnimation, 0, 200, 200, get_canvas_width() // 2, get_canvas_height() - 60)
    for i in range(SlimeNum):
        if slime[i].dead:
            slime[i].draw()
    if golemkamikaze.bomb:
        golemkamikaze.draw()
    golemsoldier.draw()
    if not golemkamikaze.bomb:
        golemkamikaze.draw()
    for i in range(SlimeNum):
        if not slime[i].expelCount and not slime[i].dead:
            slime[i].draw()
    character.draw()
    for i in range(SlimeNum):
        if not slime[i].dead and slime[i].expelCount:
            slime[i].draw()
    update_canvas()
    handle_events()
    pass

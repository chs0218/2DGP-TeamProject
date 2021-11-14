# from pico2d import *
# import random
# import Monster
#
# class Golemkamikaze:
#     slept = None
#     wake = None
#     walk = None
#     attack = None
#     die = None
#
#     def __init__(self):
#         self.x = random.randint(200, get_canvas_width() - 200)
#         self.y = random.randint(200, get_canvas_height() - 100)
#         self.animationX = 0
#         self.animationY = 0
#         self.statement = 0
#         self.bomb = False
#         self.i = 0.2
#         if Golemkamikaze.die == None:
#             Golemkamikaze.slept = load_image("monster/golemkamikaze/golemkamikaze_idleslept.png")
#             Golemkamikaze.wake = load_image("monster/golemkamikaze/golemkamikaze_wake.png")
#             Golemkamikaze.walk = load_image("monster/golemkamikaze/golemkamikaze_walk.png")
#             Golemkamikaze.attack = load_image("monster/golemkamikaze/golemkamikaze_attack.png")
#             Golemkamikaze.die = load_image("monster/golemkamikaze/kamikaze_die.png")
#
#     def draw(self):
#         if self.bomb:
#             self.die.draw(self.x, self.y)
#         else:
#             if self.statement == 0:
#                 self.slept.draw(self.x, self.y)
#             elif self.statement == 1:
#                 self.wake.clip_draw(100 * self.animationX, 0, 100, 100, self.x, self.y)
#             elif self.statement == 2:
#                 self.walk.clip_draw(100 * self.animationX, 0, 100, 100, self.x, self.y)
#             else:
#                 self.attack.clip_draw(300 * self.animationX, 300 * self.animationY, 300, 300, self.x, self.y)
#
#     def update_animation(self):
#         if self.statement == 0:
#             pass
#
#         elif self.statement == 1:
#             self.animationX += 1
#             if self.animationX == 4:
#                 self.statement = 2
#                 self.animationX = 0
#
#         elif self.statement == 2:
#             self.animationX = (self.animationX + 1) % 4
#
#         else:
#             self.animationX += 1
#             if self.animationX == 10:
#                 if self.animationY == 0:
#                     self.animationY += 1
#                 else:
#                     self.bomb = True
#                     self.animationX = 0
#                     self.animationY = 0
#                 self.animationX = 0
#
#     def move(self, character):
#         if self.statement == 0:
#             if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
#                 self.statement = 1
#
#         elif self.statement == 2:
#             t = self.i / 100
#             self.x = (1 - t) * self.x + t * character.x
#             self.y = (1 - t) * self.y + t * character.y
#
#             if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 < 6000:
#                 self.statement = 3
#                 self.animationX = 0
#             pass
#         else:
#             pass
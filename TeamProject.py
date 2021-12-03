import game_framework
import pico2d
import start_state
import result_state

Width, Height = 1276, 720

pico2d.open_canvas(Width, Height)
game_framework.play(start_state)
pico2d.close_canvas()
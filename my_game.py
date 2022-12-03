import pico2d
import game_framework

import logo_state
import stage1_state

pico2d.open_canvas()
game_framework.run(stage1_state)
pico2d.clear_canvas()
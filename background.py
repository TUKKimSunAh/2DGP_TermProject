import server
from pico2d import *

image = None

class Background_stage1:
    def __init__(self):
        self.image = load_image('Map_Stage1.png')
        self.canvas_width = 800
        self.canvas_height = 600
        self.width = 4000
        self.height = 600

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.mario.x) - self.canvas_width//2, self.width - self.canvas_width)
        self.window_bottom = clamp(0, int(server.mario.y), self.height-self.canvas_height)
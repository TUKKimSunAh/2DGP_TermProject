import server
from pico2d import *

image = None

class Background:
    def __init__(self):
        self.font = load_font('Super Mario Bros. 2.TTF', 20)
        self.marioscore = 0
        pass

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0)
        self.font.draw(20, 550, 'Score', (255, 255, 255))
        self.font.draw(20, 520, '%d' % self.marioscore, (255, 255, 255))


    def update(self):
        self.window_left = clamp(0, int(server.mario.x) - self.canvas_width//2, self.width - self.canvas_width)
        self.window_bottom = clamp(0, int(server.mario.y), self.height-self.canvas_height)

    def set_score(self, score):
        self.marioscore = score


class Stage1(Background):
    def __init__(self):
        super().__init__()

        if image == None :
            self.image = load_image("./resource/background/Map_Stage1.png")
        self.canvas_width = 800
        self.canvas_height = 600
        self.width = 4000
        self.height = 600

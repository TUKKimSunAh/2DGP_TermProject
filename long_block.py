from pico2d import *
import game_world
import server

class Long_Block:
    image = None

    def __init__(self, x, y):
        if Long_Block.image == None:
            Long_Block.image = load_image('Long_Block.png')
        self.width, self.height = 762, 90
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - 762 / 2, self.y - 90 / 2, self.x + 762 / 2, self.y + 90 / 2

    def update(self):
        if self.x < 0 or self.x > 4000:
            game_world.remove_object(self)
        pass

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        self.image.draw(sx, sy)

    def handle_collision(self, other, group):
        pass

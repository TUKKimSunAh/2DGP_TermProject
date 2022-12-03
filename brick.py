from pico2d import *
import game_world
import server

class Brick:

    def __init__(self, brick_name, x, y):
        if brick_name == 'Bricks':
            Brick.image = load_image('Bricks.png')
        if brick_name == 'Iron':
            Brick.image = load_image('Iron.png')
        if brick_name == 'Bonus_Brick':
            Brick.image = load_image('Bonus_Brick.png')

        self.width, self.height = 30, 30
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self):
        if self.x < 0 or self.x > 4000:
            game_world.remove_object(self)
        pass

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        self.image.draw(sx, sy)

    def handle_collision(self, other, group):
        pass

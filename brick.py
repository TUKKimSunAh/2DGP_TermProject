from pico2d import *
import game_world
import server

class Brick:
    image = None

    def __init__(self, x, y):
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

    def handle_collision(self, other, group, width, height):
        pass


class Normalbrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Normalbrick.image == None:
            Normalbrick.image = load_image("./resource/bricks/Bricks.png")


class Stairbrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Stairbrick.image == None:
            Stairbrick.image = load_image("./resource/bricks/Iron.png")


class Bonusmapbrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Bonusmapbrick.image == None:
            Bonusmapbrick.image = load_image("./resource/bricks/Bonus_Brick.png")


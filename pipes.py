from pico2d import *
import game_world
import server

class Pipes:
    image = None

    def __init__(self, x, y):
        self.width, self.height = 0, 0
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2

    def update(self):
        if self.x < 0 or self.x > 4000:
            game_world.remove_object(self)
        pass

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.draw(sx, sy)

    def handle_collision(self, other, group, width, height):
        pass


class Bigpipe(Pipes):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Bigpipe.image == None:
            Bigpipe.image = load_image('Pipe3.png')
        self.width, self.height = 52, 104

class Middlepipe(Pipes):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Middlepipe.image == None:
            Middlepipe.image = load_image('Pipe1.png')
        self.width, self.height = 44, 66

class Smallpipe(Pipes):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Smallpipe.image == None:
            Smallpipe.image = load_image('Pipe2.png')
        self.width, self.height = 40, 42

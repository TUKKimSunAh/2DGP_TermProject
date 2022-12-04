from pico2d import *
import game_world
import server


class Questbox:
    image = None

    def __init__(self, x, y):
        self.width, self.height = 30, 30
        self.state = 'UnDie'
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self):
        if self.x < 0 or self.x > 4000:
            game_world.remove_object(self)

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.draw(sx, sy)

    def handle_collision(self, other, group, width, height):
        pass


class Coinbox(Questbox):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Coinbox.image == None:
            Coinbox.image = load_image('QBox1.png')

    def handle_collision(self, other, group, width, height):
        pass


class Itembox(Questbox):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Itembox.image == None:
            Itembox.image = load_image('QBox2.png')
            self.breakcount = 0

    def update(self):
        super().update()
        if self.breakcount == 1:
            Itembox.image = load_image('QBox1.png')
        if self.breakcount == 2:
            Itembox.image = load_image('QBox_Die.png')

    def handle_collision(self, other, group, width, height):
        if group == 'mario:qbox2':
            if width > height:
                if self.y > other.y:
                    self.breakcount += 1
        pass


class Monsterbox(Questbox):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Monsterbox.image == None:
            Monsterbox.image = load_image('QBox3.png')


class Diebox(Questbox):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Diebox.image == None:
            Diebox.image = load_image('QBox_Die.png')

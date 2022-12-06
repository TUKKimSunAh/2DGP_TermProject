from pico2d import *
import game_world
import server

class Item:
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


class Coin(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Coin.image == None:
            Coin.image = load_image("./resource/item/Coin.png")
        self.width, self.height = 17, 30
        self.state = None
        self.frame = 0
        self.hit_cnt = 0

    def get_hitcnt(self):
        return self.hit_cnt

    def set_hitcnt(self, hitcnt):
        self.hit_cnt = hitcnt

    def set_state(self, state):
        self.state = state

    def update(self):
        super().update()
        self.frame = (self.frame + 9) % 4
        if self.hit_cnt == 2:
            game_world.remove_object(self)


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.frame * 17, 0, 17, 30, sx, sy)



    def handle_collision(self, other, group, width, height):
        if self.state == 'Hit' and group == 'mario:coin':
            self.y = self.y + 30
            self.hit_cnt += 1

            if self.hit_cnt == 2:
                other.set_score(50)
                game_world.remove_object(self)

class Flag(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Flag.image == None:
            Flag.image = load_image("./resource/item/Flag.png")
        self.width = 26
        self.height = 26


    def up(self):
        if self.y < 300:
            self.y += 5

    def handle_collision(self, other, group, width, height):
        if group == 'mario:flag':
            self.up()






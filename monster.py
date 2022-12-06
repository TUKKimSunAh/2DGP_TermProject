from pico2d import *
import game_world
import server

class Monster:
    image = None

    def __init__(self, x, y):
        self.width, self.height = 0, 0
        self.frame = 0
        self.force = 0
        self.gravity = 0.2
        self.speed = 0.5
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2

    def update(self):
        self.set_gravity()
        self.x = self.x + self.speed
        if self.x < 0 or self.x > 4000:
            game_world.remove_object(self)
        pass

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.frame * 30, 0, 30, 30, sx, sy)

    def set_gravity(self):
        self.y -= self.force
        self.force += self.gravity

    def handle_collision(self, other, group, width, height):
        if group == 'goomba:ground' or group == 'turtle:ground':
            self.y = other.y + other.height / 2 + self.height / 2
            self.force = 0

        if group == 'goomba:bigpipe' or group == 'goomba:middlepipe' or group == 'goomba:stair' or group == 'goomba:brick':
            if width < height:
                if self.x < other.x:
                    self.x = other.x - other.width / 2 - self.width / 2
                    self.speed *= -1

                else:
                    self.x = other.x + other.width / 2 + self.width / 2
                    self.speed *= -1

            else:
                if self.y < other.y:
                    self.y = other.y - other.height / 2 - self.height / 2
                    self.force = 0

                else:
                    self.y = other.y + other.height / 2 + self.height / 2
                    self.force = 0


class Goomba(Monster):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Goomba.image == None:
            Goomba.image = load_image("./resource/item/Goomba.png")
        self.width, self.height = 30, 30

    def update(self):
        super().update()
        self.frame = (self.frame + 1) % 2


class Turtle(Monster):
    def __init__(self, x, y):
        super().__init__(x, y)
        if Turtle.image == None:
            Turtle.image = load_image("./resource/item/TurtleR.png")

        self.width, self.height = 32, 32
        self.check_direction = 1
        # 왼쪽일 때 -1 오른쪽일 때 1
        self.state = 'Unhit'
        self.speed = 0.6

    def update(self):
        super().update()
        self.frame = (self.frame + 1) % 2


    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state


    def handle_collision(self, other, group, width, height):
        turtlecnt = 0

        if group == 'turtle:ground':
            self.y = other.y + other.height / 2 + self.height / 2
            self.force = 0

        if group == 'turtle:bigpipe' or group == 'turtle:middlepipe' or group == 'turtle:stair' or group == 'turtle:brick':

            if width < height:
                if self.x < other.x:
                    self.x = other.x - other.width / 2 - self.width / 2
                    self.speed *= -1

                    if turtlecnt == 0:
                        self.image = load_image("./resource/item/TurtleL.png")

                else:
                    self.x = other.x + other.width / 2 + self.width / 2
                    self.speed *= -1

                    if turtlecnt == 0:
                        self.image = load_image("./resource/item/TurtleR.png")

            else:
                if self.y < other.y:
                    self.y = other.y - other.height / 2 - self.height / 2
                    self.force = 0

                else:
                    self.y = other.y + other.height / 2 + self.height / 2
                    self.force = 0





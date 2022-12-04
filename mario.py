from pico2d import *
from questbox import Questbox
import server

stage1_width, stage1_height = 4000, 600
window_width, window_height = 800, 600

# 마리오의 방향을 확인하기 위한 변수 | 오른쪽일 경우 1, 왼쪽일 경우 -1
check_direction = 1
# 마리오의 행동을 확인하기 위한 변수 | 아이들일 경우 0, 오른쪽일 경우 1, 왼쪽일 경우 -1
check_move = 0
# 마리오의 점푸를 확인하기 위한 변수 | 아이들일 경우 0, 오른쪽 점프할 경우 1, 왼쪽 점프할 경우 -1
check_jump = 1

hitcount =0

class Mario:
    bg: object

    global check_direction, check_move, check_jump, bJump

    def __init__(self):
        self.bJump = False
        self.x, self.y = 20, 300
        self.width, self.height = 26, 26
        self.speed = 0.4
        self.frame = 0
        self.force = 0
        self.gravity = 0.05
        self.go_event = None

        self.idle_right = load_image('Mario_R.png')
        self.idle_left = load_image('Mario_L.png')
        self.walk_right = load_image('Mario_WalkR.png')
        self.walk_left = load_image('Mario_WalkL.png')
        self.jump_right = load_image('Mario_JumpR.png')
        self.jump_left = load_image('Mario_JumpL.png')

    def update(self):
        self.set_gravity()

        self.x = clamp(0, self.x, server.background.width - 1)
        self.y = clamp(0, self.y, server.background.height - 1)

        if check_move == 1:
            self.frame = (self.frame + 1) % 3
            self.x = self.x + self.speed

        elif check_move == -1:
            self.frame = (self.frame + 1) % 3
            self.x = self.x - self.speed

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if check_direction == 1:
            if check_move == 0:
                self.idle_right.draw(sx, sy)
            elif check_move == 1:
                self.walk_right.clip_draw(self.frame * 28, 0, 28, 28, sx, sy)

        elif check_direction == -1:
            if check_move == 0:
                self.idle_left.draw(sx, sy)
            elif check_move == -1:
                self.walk_left.clip_draw(self.frame * 28, 0, 28, 28, sx, sy)

        if self.bJump:
            if check_jump == 1:
                self.jump_right.draw(sx, sy)
            elif check_jump == -1:
                self.jump_left.draw(sx, sy)

    def get_bb(self):
        return self.x - 14, self.y - 14, self.x + 14, self.y + 14

    def Check_Collision_Rect(self, Src):
        fWidth = abs(self.x - Src.x)
        fHeight = abs(self.y - Src.y)

        fCX = (self.width + Src.width) * 0.5
        fCY = (self.height + Src.height) * 0.5

        if (fCX > fWidth) and (fCY > fHeight):
            pWidth = fCX - fWidth
            pHeight = fCY - fHeight

            return pWidth, pHeight

        return

    def handle_events(self, event):
        global check_direction, check_move, check_jump

        if event.type == SDL_KEYDOWN:
            if self.go_event == 'Go':
                if event.key == SDLK_a:
                    print('히 도착해따요')

            if event.key == SDLK_RIGHT:
                check_direction = 1
                check_move = 1

            if event.key == SDLK_LEFT:
                check_direction = -1
                check_move = -1

            if event.key == SDLK_SPACE:
                if check_direction == 1:
                    check_jump = 1
                elif check_direction == -1:
                    check_jump = -1

                self.force = -4.5
                self.x += 0.2
                self.bJump = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                check_move = 0

            if event.key == SDLK_SPACE:
                self.bJump = False
                check_jump = 0

    def set_gravity(self):
        self.y -= self.force
        self.force += self.gravity

    def handle_collision(self, other, group, width, height):
        global hitcount

        if group == 'mario:ground':
            self.y = other.y + other.height / 2 + self.height / 2
            self.force = 0

        if group == 'mario:brick' or group == 'mario:bigpipe' or group == 'mario:middlepipe' or group == 'mario:smallpipe':
            if width < height:
                if self.x < other.x:
                    self.x = other.x - other.width / 2 - self.width / 2

                else:
                    self.x = other.x + other.width / 2 + self.width / 2

            else:
                if self.y < other.y:
                    self.y = other.y - other.height / 2 - self.height / 2
                    self.force = 0

                else:
                    self.y = other.y + other.height / 2 + self.height / 2
                    self.force = 0
                    if group == 'mario:bigpipe':
                        self.go_event = 'Go'
                    else:
                        self.go_event = None

        if group == 'mario:qbox1':
            if self.y < other.y:
                self.y = other.y - other.height / 2 - self.height / 2
                self.force = 0
                print("캐러뜰 나 쿵해따요")
                other.image = load_image('QBox_Die.png')

            else:
                self.y = other.y + other.height / 2 + self.height / 2
                self.force = 0

        if group == 'mario:qbox2':
            print(hitcount)
            if self.y < other.y:
                self.y = other.y - other.height / 2 - self.height / 2
                self.force = 0
                hitcount += 1
                if hitcount == 1:
                    other.image = load_image('QBox1.png')
                if hitcount == 2:
                    other.image = load_image('QBox_Die.png')
                    hitcount = 0

            else:
                self.y = other.y + other.height / 2 + self.height / 2
                self.force = 0


        pass

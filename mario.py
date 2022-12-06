from pico2d import *
from questbox import Questbox
import server
import game_world

stage1_width, stage1_height = 4000, 600
window_width, window_height = 800, 600

# 마리오의 방향을 확인하기 위한 변수 | 오른쪽일 경우 1, 왼쪽일 경우 -1
check_direction = 1
# 마리오의 행동을 확인하기 위한 변수 | 아이들일 경우 0, 오른쪽일 경우 1, 왼쪽일 경우 -1
check_move = 0
# 마리오의 점푸를 확인하기 위한 변수 | 아이들일 경우 0, 오른쪽 점프할 경우 1, 왼쪽 점프할 경우 -1
check_jump = 1

hitcount = 0
qbox_state = None

class Mario:
    bg: object

    global check_direction, check_move, check_jump, bJump

    def __init__(self):
        self.bJump = False
        self.state = 'Undie'
        self.x, self.y = 20, 300
        self.width, self.height = 26, 26
        self.speed = 0.9
        self.frame = 0
        self.force = 0
        self.gravity = 0.1

        self.score = 0
        self.font = load_font('Super Mario Bros. 2.TTF', 16)
        self.go_event = None
        self.image = load_image("./resource/mario/Mario_R.png")

    def update(self):
        self.set_gravity()

        self.x = clamp(0, self.x, server.background.width - 1)
        self.y = clamp(0, self.y, server.background.height - 1)

        if self.state == 'Die':
            self.gravity = 0
            self.y += 3
            if self.y > 300:
                self.state = 'Unshow'

        if self.state == 'Unshow':
            game_world.remove_object(self)  # 이부분 게임 종료 화면 준비

        if check_move == 1:
            self.frame = (self.frame + 1) % 3
            self.x = self.x + self.speed

        elif check_move == -1:
            self.frame = (self.frame + 1) % 3
            self.x = self.x - self.speed

        if self.y < 20 or self.score < 0:
            self.state = 'Die'
            self.x = self.x - 3
            self.y = self.y + 10

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if self.state == 'Die':
            self.image = load_image("./resource/mario/Mario_Dead.png")
            self.image.draw(sx, sy)

        if check_direction == 1:
            if check_move == 0:
                self.image = load_image("./resource/mario/Mario_R.png")
                self.image.draw(sx, sy)

            elif check_move == 1:
                self.image = load_image("./resource/mario/Mario_WalkR.png")
                self.image.clip_draw(self.frame * 28, 0, 28, 28, sx, sy)

        elif check_direction == -1:
            if check_move == 0:
                self.image = load_image("./resource/mario/Mario_L.png")
                self.image.draw(sx, sy)

            elif check_move == -1:
                self.image = load_image("./resource/mario/Mario_WalkL.png")
                self.image.clip_draw(self.frame * 28, 0, 28, 28, sx, sy)

        if self.bJump:
            if check_jump == 1:
                self.image = load_image("./resource/mario/Mario_JumpR.png")
                self.image.draw(sx, sy)

            elif check_jump == -1:
                self.image = load_image("./resource/mario/Mario_JumpL.png")
                self.image.draw(sx, sy)

        self.font.draw(sx - 40, sy + 40, '%d' % self.x, (255, 255, 0))


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

    def set_gravity(self):
        self.y -= self.force
        self.force += self.gravity

    def get_score(self):
        if self.score < 0:
            self.score = 0
        return self.score

    def set_score(self, score):
        self.score = self.score + score

    def get_mariostate(self):
        return self.state

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


    def handle_collision(self, other, group, width, height):
        global hitcount, qbox_state

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

        if group == 'mario:goomba':
            time_cnt = 0
            if width < height:
                self.score -= 50
                if self.score < 0:
                    self.score = 0
                    self.image = load_image("./resource/mario/Mario_Dead.png")
                    self.state = 'Die'

            else:
                if self.y < other.y:
                    self.score -= 50

                else:
                    self.y = other.y + other.height / 2 + self.height / 2
                    self.score += 100
                    game_world.remove_object(other)

        if group == 'mario:qbox1':
            if self.y < other.y:
                self.y = other.y - other.height / 2 - self.height / 2
                self.force = 0
                other.image = load_image("./resource/box/QBox_Die.png")
                qbox_state = 'Hit'

            else:
                self.y = other.y + other.height / 2 + self.height / 2
                self.force = 0

        if group == 'mario:qbox2':
            if self.y < other.y:
                self.y = other.y - other.height / 2 - self.height / 2
                self.force = 0
                hitcount += 1
                if hitcount == 1:
                    other.image = load_image("./resource/box/QBox1.png")
                if hitcount == 2:
                    other.image = load_image("./resource/box/QBox_Die.png")

            else:
                self.y = other.y + other.height / 2 + self.height / 2
                self.force = 0

        if group == 'mario:coin':
            other.set_state(qbox_state)

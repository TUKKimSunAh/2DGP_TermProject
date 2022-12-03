from pico2d import *

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
# 마리오 점프 여부 | True, False로 판단
bJump = False

interval_width, interval_height = 0, 0


class Mario:
    bg: object

    global check_direction, check_move, check_jump, bJump

    def __init__(self):
        self.x, self.y = 20, 300
        self.width, self.height = 32, 32
        self.speed = 0.4
        self.frame = 0
        self.force = 0
        self.gravity = 0.05

        self.idle_right = load_image('Mario_R.png')
        self.idle_left = load_image('Mario_L.png')
        self.walk_right = load_image('Mario_WalkR.png')
        self.walk_left = load_image('Mario_WalkL.png')
        self.jump_right = load_image('Mario_JumpR.png')
        self.jump_left = load_image('Mario_JumpL.png')


    def update(self):
        self.set_gravity()

        self.x = clamp(0, self.x, server.background.width-1)
        self.y = clamp(0, self.y, server.background.height-1)

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
                self.walk_right.clip_draw(self.frame * 32, 0, 32, 32, sx, sy)

        elif check_direction == -1:
            if check_move == 0:
                self.idle_left.draw(sx, sy)
            elif check_move == -1:
                self.walk_left.clip_draw(self.frame * 32, 0, 32, 32, sx, sy)

        if bJump:
            if check_jump == 1:
                self.jump_right.draw(sx, sy)
            elif check_jump == -1:
                self.jump_left.draw(sx, sy)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

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
        global check_direction, check_move, check_jump, bJump
        if event.type == SDL_KEYDOWN:
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
                bJump = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                check_move = 0

            if event.key == SDLK_SPACE:
                check_jump = 0

    def set_gravity(self):
        self.y -= self.force
        self.force += self.gravity


    def handle_collision(self, other, group):
        global interval_width, interval_height

        if group == 'mario:ground':
            self.y = other.y + other.height/2 + self.height/2
            self.force = 0

        if group == 'mario:brick':
            if self.y < other.y:
                print('캐러뜰 저 쿵해따요')
                self.y = other.y - other.height / 2 - self.height / 2

            else:
                print('캐러뜰 저 올라와따여')
                self.y = other.y + other.height / 2 + self.height / 2
                self.force = 0

        pass
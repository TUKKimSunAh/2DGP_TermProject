from pico2d import *
import server
from background import Background_stage1
from mario import Mario
from long_block import Long_Block
from brick import Brick
import game_framework
import game_world
import logo_state
import manual_state


#Long_Block(381, 45), Long_Block(1905, 45)

def enter():
    server.mario = Mario()
    game_world.add_object(server.mario, 1)
    server.background = Background_stage1()
    game_world.add_object(server.background, 0)

    long_list = [Long_Block(381, 44), Long_Block(1014, 44), Long_Block(1900, 44), Long_Block(2000, 44), Long_Block(2950, 44), Long_Block(3400, 44), Long_Block(3619, 44)]
    game_world.add_objects(long_list, 1)
    game_world.add_collision_pairs(server.mario, long_list, 'mario:ground')

    brick_list = [Brick('Bricks', 180, 170), Brick('Bricks', 240, 170), Brick('Bricks', 300, 170), Brick('Bricks', 1620, 170), Brick('Bricks', 1680, 170),
                  Brick('Bricks', 1722, 340), Brick('Bricks', 1752, 340), Brick('Bricks', 1782, 340), Brick('Bricks', 1812, 340), Brick('Bricks', 1842, 340), Brick('Bricks', 1872, 340), Brick('Bricks', 1902, 340),
                  Brick('Bricks', 1932, 340), Brick('Bricks', 1962, 340), Brick('Bricks', 1992, 340)]
    game_world.add_objects(brick_list, 2)
    game_world.add_collision_pairs(server.mario, brick_list, 'mario:brick')


def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()

    for event in events:
        server.mario.handle_events(event)

        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(logo_state)

            if event.key == SDLK_m:
                game_framework.push_state(manual_state)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True




def update():

    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

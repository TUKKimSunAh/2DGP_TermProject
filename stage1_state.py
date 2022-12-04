from pico2d import *
import server
from background import Background_stage1
from mario import Mario
from long_block import Long_Block
from brick import Normalbrick
from brick import Stairbrick
from questbox import Coinbox
from questbox import Itembox
from pipes import Bigpipe
from pipes import Middlepipe
from pipes import Smallpipe


import game_framework
import game_world
import logo_state
import manual_state


def enter():
    server.background = Background_stage1()
    game_world.add_object(server.background, 0)

    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    middelepipe_list = [Middlepipe(550, 110), Middlepipe(780, 122)]
    game_world.add_objects(middelepipe_list, 3)
    game_world.add_collision_pairs(server.mario, middelepipe_list, 'mario:middlepipe')

    bigpipe_list = [Bigpipe(990, 141)]
    game_world.add_objects(bigpipe_list, 4)
    game_world.add_collision_pairs(server.mario, bigpipe_list, 'mario:bigpipe')

    long_list = [Long_Block(381, 44), Long_Block(1014, 44), Long_Block(1900, 44), Long_Block(2000, 44), Long_Block(2950, 44), Long_Block(3400, 44), Long_Block(3619, 44)]
    game_world.add_objects(long_list, 5)
    game_world.add_collision_pairs(server.mario, long_list, 'mario:ground')

    brick_list = [Normalbrick(180, 170), Normalbrick(240, 170), Normalbrick(300, 170),
                  Normalbrick(1620, 170), Normalbrick(1680, 170),
                  Normalbrick(1722, 340), Normalbrick(1752, 340), Normalbrick(1782, 340), Normalbrick(1812, 340), Normalbrick(1842, 340), Normalbrick(1872, 340), Normalbrick(1902, 340),
                  Normalbrick(1932, 340), Normalbrick(1962, 340), Normalbrick(1992, 340)]
    game_world.add_objects(brick_list, 6)
    game_world.add_collision_pairs(server.mario, brick_list, 'mario:brick')

    coinbox_list = [Coinbox(210, 170), Coinbox(270, 170),
                    Coinbox(1650, 170), Coinbox(1710, 170)]
    game_world.add_objects(coinbox_list, 7)
    game_world.add_collision_pairs(server.mario, coinbox_list, 'mario:qbox1')

    itembox_list = [Itembox(1752, 450)]
    game_world.add_objects(itembox_list, 8)
    game_world.add_collision_pairs(server.mario, itembox_list, 'mario:qbox2')

    stairlist_list = [Stairbrick(1200, 104), Stairbrick(1230, 104), Stairbrick(1260, 104), Stairbrick(1290, 104), Stairbrick(1320, 104),
                      Stairbrick(1260, 104), Stairbrick(1290, 104), Stairbrick(1320, 104), Stairbrick(1350, 104), Stairbrick(1380, 104),
                      Stairbrick(1230, 134), Stairbrick(1260, 134), Stairbrick(1290, 134), Stairbrick(1320, 134), Stairbrick(1350, 134), Stairbrick(1380, 134),
                      Stairbrick(1260, 164), Stairbrick(1290, 164), Stairbrick(1320, 164), Stairbrick(1350, 164), Stairbrick(1380, 164),
                      Stairbrick(1290, 194), Stairbrick(1320, 194), Stairbrick(1350, 194), Stairbrick(1380, 194),
                      Stairbrick(1320, 224), Stairbrick(1350, 224), Stairbrick(1380, 224),
                      Stairbrick(1350, 254), Stairbrick(1380, 254), Stairbrick(1380, 284)]
    game_world.add_objects(stairlist_list, 9)
    game_world.add_collision_pairs(server.mario, stairlist_list, 'mario:middlepipe')






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

def Check_Collision_Rect(self, Src):
    fWidth = abs(self.x - Src.x)
    fHeight = abs(self.y - Src.y)

    fCX = (self.width + Src.width) * 0.5
    fCY = (self.height + Src.height) * 0.5

    if (fCX > fWidth) and (fCY > fHeight):
        pWidth = fCX - fWidth
        pHeight = fCY - fHeight

        return 'Hit', pWidth, pHeight

    return 'Unhit', 0, 0


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        hit_judge, interval_width, interval_height = Check_Collision_Rect(a, b)

        if 'Hit' == hit_judge:
            a.handle_collision(b, group, interval_width, interval_height)
            b.handle_collision(a, group, interval_width, interval_height)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

from pico2d import *
import server
import time

from background import Stage1
from mario import Mario
#from items import Flag
from long_block import Long_Block
from brick import Normalbrick
from brick import Stairbrick
from questbox import Coinbox
from questbox import Itembox
from pipes import Bigpipe
from pipes import Middlepipe
#from monster import Goomba
#from monster import Turtle
from item import Coin


import title_state
import game_framework
import game_world
import logo_state
import manual_state


def enter():
    server.background = Stage1()
    game_world.add_object(server.background, 0)

    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    middelepipe_list = [Middlepipe(550, 110), Middlepipe(780, 122), Bigpipe(2360, 141), Middlepipe(2826, 122),
                        Middlepipe(3400, 122), Middlepipe(3600, 110)]
    game_world.add_objects(middelepipe_list, 3)
    game_world.add_collision_pairs(server.mario, middelepipe_list, 'mario:middlepipe')

    bigpipe_list = [Bigpipe(1014, 141)]
    game_world.add_objects(bigpipe_list, 4)
    game_world.add_collision_pairs(server.mario, bigpipe_list, 'mario:bigpipe')

    long_list = [Long_Block(381, 44), Long_Block(1014, 44), Long_Block(1900, 44), Long_Block(2000, 44),
                 Long_Block(2950, 44), Long_Block(3400, 44), Long_Block(3619, 44)]
    game_world.add_objects(long_list, 5)
    game_world.add_collision_pairs(server.mario, long_list, 'mario:ground')

    brick_list = [Normalbrick(180, 170), Normalbrick(240, 170), Normalbrick(300, 170), Normalbrick(1620, 170),
                  Normalbrick(1680, 170),
                  Normalbrick(1722, 300), Normalbrick(1752, 300), Normalbrick(1782, 300), Normalbrick(1812, 300),
                  Normalbrick(1842, 300), Normalbrick(1872, 300), Normalbrick(1902, 300),
                  Normalbrick(1932, 300), Normalbrick(1820, 450), Normalbrick(1850, 450), Normalbrick(1880, 450),
                  Normalbrick(2950, 260), Normalbrick(2980, 260), Normalbrick(3010, 260),
                  Normalbrick(3070, 340), Normalbrick(3100, 340), Normalbrick(3130, 340),
                  Normalbrick(3190, 420), Normalbrick(3220, 420), Normalbrick(3250, 420)]
    game_world.add_objects(brick_list, 6)
    game_world.add_collision_pairs(server.mario, brick_list, 'mario:brick')

    coin_list = [Coin(210, 169), Coin(270, 169), Coin(1650, 169), Coin(1710, 169)]
    game_world.add_objects(coin_list, 7)
    game_world.add_collision_pairs(server.mario, coin_list, 'mario:coin')

    coinbox_list = [Coinbox(210, 170), Coinbox(270, 170),
                    Coinbox(1650, 170), Coinbox(1710, 170)]
    game_world.add_objects(coinbox_list, 11)
    game_world.add_collision_pairs(server.mario, coinbox_list, 'mario:qbox1')

    itembox_list = [Itembox(1790, 450)]
    game_world.add_objects(itembox_list, 8)
    game_world.add_collision_pairs(server.mario, itembox_list, 'mario:qbox2')

    stairlist_list = [Stairbrick(1200, 104), Stairbrick(1230, 104), Stairbrick(1260, 104), Stairbrick(1290, 104),
                      Stairbrick(1320, 104),
                      Stairbrick(1260, 104), Stairbrick(1290, 104), Stairbrick(1320, 104), Stairbrick(1350, 104),
                      Stairbrick(1380, 104),
                      Stairbrick(1230, 134), Stairbrick(1260, 134), Stairbrick(1290, 134), Stairbrick(1320, 134),
                      Stairbrick(1350, 134), Stairbrick(1380, 134),
                      Stairbrick(1260, 164), Stairbrick(1290, 164), Stairbrick(1320, 164), Stairbrick(1350, 164),
                      Stairbrick(1380, 164),
                      Stairbrick(1290, 194), Stairbrick(1320, 194), Stairbrick(1350, 194), Stairbrick(1380, 194),
                      Stairbrick(1320, 224), Stairbrick(1350, 224), Stairbrick(1380, 224),
                      Stairbrick(1350, 254), Stairbrick(1380, 254), Stairbrick(1380, 284),
                      Stairbrick(2100, 104), Stairbrick(2130, 104), Stairbrick(2160, 104), Stairbrick(2190, 104),
                      Stairbrick(2100, 134), Stairbrick(2130, 134), Stairbrick(2160, 134),
                      Stairbrick(2100, 164), Stairbrick(2130, 164), Stairbrick(2100, 194),
                      Stairbrick(2580, 104), Stairbrick(2610, 104), Stairbrick(2640, 104), Stairbrick(2670, 104),
                      Stairbrick(2610, 134), Stairbrick(2640, 134), Stairbrick(2670, 134),
                      Stairbrick(2640, 164), Stairbrick(2670, 164), Stairbrick(2670, 194)
                      ]
    game_world.add_objects(stairlist_list, 9)
    game_world.add_collision_pairs(server.mario, stairlist_list, 'mario:brick')





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

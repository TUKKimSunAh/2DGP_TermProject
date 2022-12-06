from pico2d import *

import game_framework
import stage1_state
import title_state


image = None

def enter():
    global image
    image = load_image("./resource/baackground/manual.png")

def exit():
    global image
    del image
    pass

def update():
    stage1_state.update()
    pass

def draw():
    clear_canvas()
    stage1_state.draw_world()
    image.draw(400, 500)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key== SDLK_m:
                    game_framework.pop_state()
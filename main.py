import os
# from tensorflow import keras
import time
import pygame as pg
import random as rnd
import threading

from Creature import Creature
from SimpleNN import SimpleNN
from ViewDirection import ViewDirection
from CreaturesField import CreaturesField
from DrawScene import DrawScene

# pip freeze > requirements.txt
# pip install -r requirements.txt

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
DRAW_FPS = 60
CALC_FPS = 60

FIELD_BLOCK_SIZE = 5
FIELD_BLOCK_MARGIN = 0
FIELD_BORDER_MARGIN = 5

running = True


def handle_events(draw_scene: DrawScene, creatures_field: CreaturesField):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key == pg.K_HOME:
                draw_scene.left = 0
                draw_scene.top = 0

        if event.type != pg.MOUSEMOTION:
            # print(f"{draw_scene.left} {draw_scene.top}")
            pass

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        draw_scene.left -= 1
    elif keys[pg.K_RIGHT]:
        draw_scene.left += 1
    elif keys[pg.K_UP]:
        draw_scene.top -= 1
    elif keys[pg.K_DOWN]:
        draw_scene.top += 1

    return True


def thread_all(creatures_field: CreaturesField):
    global running

    print("thread_all started")
    while running:
        creatures_field.do_one_step()
        pg.display.set_caption(
            f"Creatures {creatures_field.width} x {creatures_field.height} Count={creatures_field.creatures_count}")
        #print("thread_all one step")

    print("thread_all done")


def main():
    global running
    creatures_field = CreaturesField(240, 160, FIELD_BLOCK_SIZE, FIELD_BLOCK_MARGIN, FIELD_BORDER_MARGIN)

    _ = Creature(None)
    _ = ViewDirection()

    # for i in range(100):
    for i in range(creatures_field.width * creatures_field.height // 3):

        # model = keras.Sequential()
        # model.add(keras.layers.Dense(units=len(Creature.dict_input) * 2, activation="relu",
        #                              input_dim=len(Creature.dict_input), use_bias=True))
        # model.add(keras.layers.Dense(units=len(Creature.dict_output) * 2, activation="relu", use_bias=True))
        # model.add(keras.layers.Dense(units=len(Creature.dict_output) * 2, activation="relu", use_bias=True))
        # model.add(keras.layers.Dense(units=len(Creature.dict_output), activation="softmax"))
        # model.compile(loss="mean_squared_error", optimizer=keras.optimizers.Adam(0.01))

        model = SimpleNN(len(Creature.dict_input))
        model.add(len(Creature.dict_input) * 2 - 1, activation="relu", use_bias=True)
        model.add(len(Creature.dict_output) * 2 + 1, activation="relu", use_bias=False)
        model.add(len(Creature.dict_output), activation="softmax")

        creature = Creature(model, (rnd.randrange(255), rnd.randrange(255), rnd.randrange(255)))
        creatures_field[(rnd.randrange(creatures_field.width), rnd.randrange(creatures_field.height))] = creature

    pg.init()
    sc = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(f"Creatures {creatures_field.width} x {creatures_field.height}")
    clock = pg.time.Clock()

    draw_scene = DrawScene(sc)

    tic = time.perf_counter()
    delay = 1.0 / CALC_FPS

    # thread_one_step = threading.Thread(target=thread_all, name="thread_one_step", args=creatures_field)
    # thread_one_step.start()

    age = 0
    while running:
        clock.tick(DRAW_FPS)
        running = handle_events(draw_scene, creatures_field)

        creatures_field.do_one_step()
        pg.display.set_caption(
            f"Creatures {creatures_field.width} x {creatures_field.height} Count={creatures_field.creatures_count} Age={age}")
        age += 1
        print("thread_all one step")

        # print(threading.enumerate())
        # print(threading.enumerate())
        # toc = time.perf_counter()
        # if toc - tic > delay and not thread_one_step.is_alive():
        #     pg.display.set_caption(
        #         f"Creatures {creatures_field.width} x {creatures_field.height} Count={creatures_field.creatures_count}")
        #     thread_one_step.start()
        #     print(threading.enumerate())
        #     tic = time.perf_counter()

        draw_scene.draw(creatures_field)


pg.quit()

main()

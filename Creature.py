import os
import numpy as np
import random as rnd
from tensorflow import keras
from ViewDirection import ViewDirection

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


class Creature:
    def __init__(self, brain: keras.Model, color: tuple = (100, 100, 100), health: int = 100):
        if not hasattr(Creature, '_id'):
            Creature._id = 0
        Creature._id += 1
        self._id = Creature._id
        print(f"ID: {self._id}")
        #
        self._moved = False
        self._color = color
        self._view_direction = 0
        self._health = health
        self._brain = brain
        #
        Creature.dict_input = {
            "HEALTH": 0,
            "PHOTOSYNTHESIS_LEVEL": 1,
            # wall 1 exists 0 none
            "WALL_FORWARD1": 2,
            "WALL_LEFT": 3,
            "WALL_RIGHT": 4,
            # creature 1 exists 0 empty
            "ANY_FORWARD1": 5,
            "ANY_FORWARD2": 6,
            "ANY_LEFT": 7,
            "ANY_RIGHT": 8,
            # class creature 1 my 0 not
            "MY_FORWARD1": 9,
            "MY_FORWARD2": 10,
            "MY_LEFT": 11,
            "MY_RIGHT": 12
        }
        #
        Creature.dict_output = {
            "STAY": 0,
            "ROTATE_LEFT": 1,
            "ROTATE_RIGHT": 2,
            "MOVE_FORWARD": 3,
            "EAT": 4,
            "DUPLICATE": 5,
            "PHOTOSYNTHESIS": 6
        }

    @property
    def id(self):
        return self._id

    @property
    def moved(self):
        return self._moved

    @moved.setter
    def moved(self, value):
        self._moved = value

    def do_one_step(self, pos_x: int, pos_y: int, matrix: np.ndarray):
        if self._moved:
            return False
        self._moved = True

        self._health -= 1
        if self._health <= 0:
            matrix[pos_x, pos_y] = None
            return True

        input_vector = np.zeros((1, len(Creature.dict_input)))
        input_vector[0, Creature.dict_input['HEALTH']] = self._health / 100.0
        input_vector[0, Creature.dict_input['PHOTOSYNTHESIS_LEVEL']] = 1.0

        output_vector = self._brain.predict(input_vector, verbose=0)
        action = output_vector.argmax()

        if action == Creature.dict_output['STAY']:
            return False
        elif action == Creature.dict_output['PHOTOSYNTHESIS']:
            self.health += 10
            return False
        elif action == Creature.dict_output['ROTATE_LEFT']:
            self._view_direction = ViewDirection.rotate(self._view_direction, -1)
            return True
        elif action == Creature.dict_output['ROTATE_RIGHT']:
            self._view_direction = ViewDirection.rotate(self._view_direction, 1)
            return True
        else:
            x, y = ViewDirection.add_delta(self._view_direction, (pos_x, pos_y))
            if 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1]:
                if action == Creature.dict_output['MOVE_FORWARD']:
                    if matrix[x, y] is None:
                        matrix[pos_x, pos_y] = None
                        matrix[x, y] = self
                        return True
                elif action == Creature.dict_output['EAT']:
                    if matrix[x, y] is not None:
                        matrix[x, y] = None
                        self.health += 50
                        return True
                elif action == Creature.dict_output['DUPLICATE']:
                    if self._health > 50 and matrix[x, y] is None:
                        creature = Creature(self._brain, self._color, self._health // 2)
                        matrix[x, y] = creature
                        self._health -= creature.health
                        return True
        return False

    @property
    def color(self):
        return self._color

    @property
    def move_direction(self):
        return self._view_direction

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value
        if self._health > 100:
            self._health = 100
        if self._health < 0:
            self._health = 0

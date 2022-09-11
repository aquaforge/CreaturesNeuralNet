import os
import numpy as np
from SimpleNN import SimpleNN
# from tensorflow import keras
from ViewDirection import ViewDirection

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

class Creature:
    def __init__(self, brain: SimpleNN, color: tuple = (200, 100, 200), health: int = 100):
        if not hasattr(Creature, '_id'):
            Creature._id = 0
        Creature._id += 1
        self._id = Creature._id
        self._moved = False

        self._color = color
        self._view_direction = 0
        self._age = 1
        self._health = health
        self._brain = brain
        #
        Creature.dict_input = {
            "HEALTH": 0,
            "PHOTOSYNTHESIS_LEVEL": 1,
            "WALL_AHEAD": 2,
            "ANY_AHEAD": 3,
            "ANY_LEFT": 4,
            "ANY_RIGHT": 5,
            "MY_AHEAD": 6,
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
    def health(self):
        return self._health

    @property
    def color(self):
        return self._color

    @health.setter
    def health(self, value: int):
        self._health = value
        if self._health > 100:
            self._health = 100
        if self._health < 0:
            self._health = 0

    @property
    def id(self):
        return self._id

    @property
    def moved(self):
        return self._moved

    @moved.setter
    def moved(self, value):
        self._moved = value

    @staticmethod
    def in_field(pos: tuple, matrix: np.ndarray):
        return 0 <= pos[0] < matrix.shape[0] and 0 <= pos[1] < matrix.shape[1]

    def do_one_step(self, pos_x: int, pos_y: int, matrix: np.ndarray):
        if self._moved:
            return
        self._moved = True

        self._health -= 1
        if self._health <= 0:
            matrix[pos_x, pos_y] = None
            return

        self._age += 1

        input_vector = np.zeros((1, len(Creature.dict_input)))
        input_vector[0, Creature.dict_input['HEALTH']] = self._health / 100.0
        input_vector[0, Creature.dict_input['PHOTOSYNTHESIS_LEVEL']] = 1.0

        d = self._view_direction
        a = ViewDirection.add_delta(d, (pos_x, pos_y))
        l = ViewDirection.add_delta(ViewDirection.rotate(d, -1), (pos_x, pos_y))
        r = ViewDirection.add_delta(ViewDirection.rotate(d, 1), (pos_x, pos_y))

        if Creature.in_field(a, matrix) and matrix[a[0], a[1]] is not None:
            input_vector[0, Creature.dict_input["ANY_AHEAD"]] = 1

        if Creature.in_field(l, matrix) and matrix[l[0], l[1]] is not None:
            input_vector[0, Creature.dict_input["ANY_LEFT"]] = 1

        if Creature.in_field(r, matrix) and matrix[r[0], r[1]] is not None:
            input_vector[0, Creature.dict_input["ANY_RIGHT"]] = 1

        # input_vector[0, Creature.dict_input["MY_AHEAD"]] = 0

        output_vector = self._brain.predict(input_vector, verbose=0)
        action = output_vector.argmax()

        if action == Creature.dict_output['STAY']:
            return
        elif action == Creature.dict_output['PHOTOSYNTHESIS']:
            self.health += 10
            return
        elif action == Creature.dict_output['ROTATE_LEFT']:
            self._view_direction = ViewDirection.rotate(self._view_direction, -1)
            return
        elif action == Creature.dict_output['ROTATE_RIGHT']:
            self._view_direction = ViewDirection.rotate(self._view_direction, 1)
            return
        else:
            x, y = ViewDirection.add_delta(self._view_direction, (pos_x, pos_y))
            if Creature.in_field((x, y), matrix):
                if action == Creature.dict_output['MOVE_FORWARD']:
                    if matrix[x, y] is None:
                        matrix[pos_x, pos_y] = None
                        matrix[x, y] = self
                        return
                elif action == Creature.dict_output['EAT']:
                    if matrix[x, y] is not None:
                        matrix[x, y] = None
                        self.health += 50
                        return
                elif action == Creature.dict_output['DUPLICATE']:
                    if self._health > 50 and matrix[x, y] is None:
                        creature = Creature(self._brain, self._color, self._health // 2)
                        matrix[x, y] = creature
                        self._health -= creature.health
                        return
        return

    # @property
    # def move_direction(self):
    #     return self._view_direction

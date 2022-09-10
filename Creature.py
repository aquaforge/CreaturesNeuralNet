import os
import numpy as np
import random as rnd
from tensorflow import keras
# import matplotlib.pyplot as plt

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"




# import uuid
# >>> # make a random UUID
# >>> uuid.uuid4()
# UUID('bd65600d-8669-4903-8a14-af88203add38')
#
# >>> # Convert a UUID to a string of hex digits in standard form
# >>> str(uuid.uuid4())
# 'f50ec0b7-f960-400d-91f0-c42a6d44e3d0'
#
# >>> # Convert a UUID to a 32-character hexadecimal string
# >>> uuid.uuid4().hex
# '9fe2c4e93f654fdbb24c02b15259716c'


from enums import MoveDirection


class Creature:
    def __init__(self, color=(200, 200, 200), move_direction: MoveDirection = MoveDirection.UP):
        if not hasattr(Creature, '_id'):
            Creature._id = 0
        Creature._id += 1
        self._id = Creature._id
        print(f"ID: {self._id}")
        #
        self._moved = False
        self._color = color
        self._move_direction = MoveDirection(move_direction)

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
        x = pos_x
        y = pos_y
        if self._move_direction == MoveDirection.UP:
            x -= 1
        elif self._move_direction == MoveDirection.DOWN:
            x += 1
        elif self._move_direction == MoveDirection.LEFT:
            y -= 1
        elif self._move_direction == MoveDirection.RIGHT:
            y += 1
        if 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1] and (pos_x != x or pos_y != y):
            matrix[pos_x, pos_y] = None
            matrix[x, y] = self
            return True
        return False

    @property
    def color(self):
        return self._color

    @property
    def move_direction(self):
        return self._move_direction

    # @property
    # def x(self):
    #     return self._x
    #
    # @x.setter
    # def x(self, value):
    #     self._x = value
    #
    # @property
    # def y(self):
    #     return self._y
    #
    # @y.setter
    # def y(self,value):
    #     self._y = value

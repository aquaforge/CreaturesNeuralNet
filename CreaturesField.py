import pygame as pg
import numpy as np
import datetime

from Creature import Creature

COLOR_NONE = (125, 125, 125)


class CreaturesField:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._age = 0

        # self._set_draw_size()
        self._matrix = np.empty((self._width, self._height), dtype=Creature)
        self.matrix_creatures_color = np.empty((self._width, self._height), dtype=object)
        self._prepare_matrix_creatures_color()
        self._need_redraw = True

    def _prepare_matrix_creatures_color(self):
        for h in range(self._height):
            for w in range(self._width):
                creature: Creature = self[(w, h)]
                if not (creature is None):
                    self.matrix_creatures_color[w, h] = creature.color
                else:
                    self.matrix_creatures_color[w, h] = COLOR_NONE

    def do_one_step(self):
        for h in range(self._height):
            for w in range(self._width):
                creature: Creature = self[(w, h)]
                if not (creature is None):
                    creature.moved = False

        for h in range(self._height):
            for w in range(self._width):
                creature: Creature = self[(w, h)]
                if not (creature is None):
                    creature.do_one_step(w, h, self._matrix)

        self._prepare_matrix_creatures_color()

        self._age += 1
        self._need_redraw = True

    @property
    def age(self):
        return self._age

    @property
    def creatures_count(self):
        return np.count_nonzero(self._matrix)

    @property
    def need_redraw(self):
        return self._need_redraw

    def redrawed(self):
        self._need_redraw = False

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __setitem__(self, pos, value: Creature):
        self._matrix[pos[0], pos[1]] = value

    def __getitem__(self, pos):
        return self._matrix[pos[0], pos[1]]

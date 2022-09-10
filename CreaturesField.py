import pygame as pg
import numpy as np
import datetime

from Creature import Creature

GREY = (125, 125, 125)
RED = (255, 0, 0)


class CreaturesField:
    def __init__(self, width: int, height: int, block_size: int, margin_inner: int, margin_outer: int):
        self._width = width
        self._height = height
        self._need_redraw = True
        self._changed = True
        self._block_size = block_size
        self._margin_inner = margin_inner
        self._margin_outer = margin_outer

        self._set_draw_size()
        self._surf = None
        self._matrix = np.empty((self._width, self._height), dtype=Creature)

    def do_one_step(self):
        for h in range(self._height):
            for w in range(self._width):
                creature: Creature = self[(w, h)]
                if not (creature is None):
                    creature.moved = False

        changed = False
        for h in range(self._height):
            for w in range(self._width):
                creature: Creature = self[(w, h)]
                if not (creature is None):
                    if creature.do_one_step(w, h, self._matrix):
                        changed = True
        if changed:
            self._changed = True

    def __setitem__(self, pos, value: Creature):
        # v: Creature = self._matrix[pos[0], pos[1]]
        # if v is not None:
        #     v.x = -1
        #     v.y = -1
        # if value is not None:
        #     value.x = pos[0]
        #     value.y = pos[1]
        self._matrix[pos[0], pos[1]] = value
        self._changed = True

    def __getitem__(self, pos):
        return self._matrix[pos[0], pos[1]]

    def _set_draw_size(self):
        self._draw_size = (
            2 * self._margin_outer - self._margin_inner + self._width * (
                    self._block_size + self._margin_inner),
            2 * self._margin_outer - self._margin_inner + self._height * (
                    self._block_size + self._margin_inner)
        )

    @property
    def creatures_count(self):
        return np.count_nonzero(self._matrix)

    @property
    def need_redraw(self):
        return self._need_redraw

    @need_redraw.setter
    def need_redraw(self, value):
        self._need_redraw = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def block_size(self):
        return self._block_size

    @property
    def margin_inner(self):
        return self._margin_inner

    @property
    def margin_outer(self):
        return self._margin_outer

    @block_size.setter
    def block_size(self, value):
        if value < 1:
            value = 1
        if self._block_size != value:
            self._block_size = value
            self._changed = True
            self._set_draw_size(self)

    @margin_inner.setter
    def margin_inner(self, value):
        if value < 0:
            value = 0
        if self._margin_inner != value:
            self._margin_inner = value
            self._changed = True
            self._set_draw_size(self)

    @margin_outer.setter
    def margin_outer(self, value):
        if value < 5:
            value = 5
        if self._margin_outer != value:
            self._margin_outer = value
            self._changed = True
            self._set_draw_size(self)

    @property
    def surf(self):
        if self._surf is None:
            self._surf = pg.Surface(self._draw_size)
            self._changed = True
        elif (self._surf.get_width(), self._surf.get_height()) != self._draw_size:
            self._surf = pg.Surface(self._draw_size)
            self._changed = True

        if self._changed:
            self._surf.fill(RED)
            for h in range(self._height):
                for w in range(self._width):
                    color = GREY
                    if self._matrix[w, h] is not None:
                        color = self._matrix[w, h].color

                    pg.draw.rect(self._surf, color, (
                        self._margin_outer + w * (self._block_size + self._margin_inner),
                        self._margin_outer + h * (self._block_size + self._margin_inner),
                        self._block_size,
                        self._block_size))
            self._changed = False
            self._need_redraw = True
            print("cr_redraw")

        return self._surf

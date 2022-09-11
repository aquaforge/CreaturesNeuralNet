import pygame as pg
from CreaturesField import CreaturesField

COLOR_BACKGROUND = (0, 0, 0)

class DrawScene:
    def __init__(self, sc: pg.Surface):
        self._sc = sc
        self._left = 0
        self._top = 0
        self._need_redraw = True

    def draw(self, creatures_field : CreaturesField):
        surf = creatures_field.surf
        if creatures_field.need_redraw or self._need_redraw:
            self._sc.fill(COLOR_BACKGROUND)
            self._sc.blit(surf, (self._left, self._top))
            pg.display.update()
            self._need_redraw = False
            creatures_field.need_redraw = False
            print("sc_redraw")

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @left.setter
    def left(self, left: int):
        if self._left != left:
            self._need_redraw = True
            self._left = left

    @top.setter
    def top(self, top: int):
        if self._top != top:
            self._need_redraw = True
            self._top = top

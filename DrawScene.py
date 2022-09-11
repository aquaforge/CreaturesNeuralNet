import pygame as pg
from CreaturesField import CreaturesField

COLOR_BACKGROUND = (0, 0, 0)
COLOR_BORDER = (255, 0, 0)


class DrawScene():
    def __init__(self, sc: pg.Surface, creatures_field: CreaturesField, block_size: int, margin_inner: int,
                 margin_outer: int):
        self._sc = sc
        self._left = 0
        self._top = 0
        self._need_redraw = True

        self._creatures_field = creatures_field
        self._surf = None

        self._block_size = block_size
        self._margin_inner = margin_inner
        self._margin_outer = margin_outer
        self._get_surf_size()

    def _get_surf_size(self):
        self._draw_size = (
            2 * self._margin_outer - self._margin_inner + self._creatures_field.width * (
                    self._block_size + self._margin_inner),
            2 * self._margin_outer - self._margin_inner + self._creatures_field.height * (
                    self._block_size + self._margin_inner)
        )

    def draw(self):
        self._prepare_surf()
        if self._need_redraw:
            self._sc.fill(COLOR_BACKGROUND)
            if self._surf is not None:
                self._sc.blit(self._surf, (self._left, self._top))
            pg.display.update()
            self._need_redraw = False
            pg.display.set_caption(
                f"Creatures {self._creatures_field.width} x {self._creatures_field.height} Count={self._creatures_field.creatures_count} Age={self._creatures_field.age}")
            # print("sc_redraw")

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

    def _prepare_surf(self):
        changed = False
        if self._surf is None:
            self._surf = pg.Surface(self._draw_size)
            changed = True
        elif (self._surf.get_width(), self._surf.get_height()) != self._draw_size:
            self._surf = pg.Surface(self._draw_size)
            changed = True

        if changed or self._creatures_field.need_redraw:
            self._surf.fill(COLOR_BORDER)
            for h in range(self._creatures_field.height):
                for w in range(self._creatures_field.width):
                    pg.draw.rect(self._surf, self._creatures_field.matrix_creatures_color[w, h], (
                        self._margin_outer + w * (self._block_size + self._margin_inner),
                        self._margin_outer + h * (self._block_size + self._margin_inner),
                        self._block_size,
                        self._block_size))
            self._creatures_field.redrawed()
            self._need_redraw = True


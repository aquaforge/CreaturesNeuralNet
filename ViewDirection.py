from enum import Enum


class ViewDirection:
    def __init__(self):
        ViewDirection.dict_direction = {
            "UP": 0,
            "RIGHT": 1,
            "DOWN": 2,
            "LEFT": 3
        }

    @staticmethod
    def add_delta(direction: int, pos: tuple = (0, 0)):
        x = pos[0]
        y = pos[1]
        if direction == ViewDirection.dict_direction['UP']:
            x -= 1
        elif direction == ViewDirection.dict_direction['DOWN']:
            x += 1
        elif direction == ViewDirection.dict_direction['LEFT']:
            y -= 1
        elif direction == ViewDirection.dict_direction['RIGHT']:
            y += 1
        return x, y

    @staticmethod
    # - left, + right
    def rotate(direction: int, rotation: int):
        return (direction + rotation) % len(ViewDirection.dict_direction)

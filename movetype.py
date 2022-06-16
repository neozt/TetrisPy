from enum import Enum


class MoveType(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    ROTATE_CW = 'rotate_cw'
    ROTATE_CCW = 'rotate_ccw'

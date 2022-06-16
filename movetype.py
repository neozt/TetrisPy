from enum import Enum


class MoveType(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    ROTATE_CW = 'rotate_cw'
    ROTATE_CCW = 'rotate_ccw'
    ROTATE_180 = 'rotate_180'

    def is_rotation(self):
        return self in {self.ROTATE_CW, self.ROTATE_CCW, self.ROTATE_180}

    def is_movement(self):
        return self in {self.LEFT, self.RIGHT, self.DOWN}

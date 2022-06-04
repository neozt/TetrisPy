from abc import ABC, abstractmethod, abstractproperty, abstractstaticmethod
from board import Board

class Mino(ABC):
    MINO_UP = 0
    MINO_RIGHT = 1
    MINO_DOWN = 2
    MINO_LEFT = 3

    def __init__(self, board, center = None, orientation = None):
        if center is None or orientation is None:
            self.center = self.spawn_position()
            self.orientation = self.spawn_orientation()
        else:
            self.center = center
            self.orientation = orientation
        self.prev_center = None
        self.prev_orientation = None
        self.board = board
    
    def __repr__(self):
        return f'[{type(self).__name__}, position = {self.center}, orientation = {self.orientation}]'

    def __str__(self):
        return str(type(self).__name__)
        
    @abstractstaticmethod
    def spawn_position():
        pass

    @classmethod
    def spawn_orientation(cls):
        return cls.MINO_UP

    @classmethod
    def spawn(cls, board):
        return cls(board)

    @property
    @abstractmethod
    def block_positions(self):
        pass

    @staticmethod
    def offset(center, x, y):
        center_x, center_y = center
        return (center_x + x, center_y + y)

    def offset_from_center(self, offset):
        return (self.center[0] + offset[0], self.center[1] + offset[1])

    def save_state(self):
        self.prev_center = self.center
        self.prev_orientation = self.orientation

    def restore_state(self):
        if self.prev_center is None or self.prev_orientation is None:
            raise Exception("No saved state to restore")
        self.center = self.prev_center
        self.orientation = self.prev_orientation
        self.prev_center = None
        self.prev_orientation = None

    def check_collision(self):
        board = self.board
        for block in self.block_positions:
            inside_row_limit = ( block[0] < Board.ROWS )
            inside_col_limit = ( 0 <= block[1] < Board.COLUMNS )
            if not inside_row_limit or not inside_col_limit:
                return True

            cell_already_occupied = board.is_occupied(block)
            if cell_already_occupied:
                return True

        return False

    def move(self, direction):
        self.save_state()

        if direction == 'left':
            offset = (0, -1)
        elif direction == 'right':
            offset = (0, 1)
        elif direction == 'down':
            offset = (1, 0)
        else:
            raise Exception('Invalid Mino move direction')

        self.center = self.offset_from_center(offset)
        success = not self.check_collision()
        if (not success):
            # print(f'Couldn\'t move {direction}')
            self.restore_state()
        return success

    def rotate_cw(self):
        self.save_state()
        self.orientation = (self.orientation + 1) % 4
        success = not self.check_collision()
        if (not success):
            print(f'Couldn\'t rotate clockwise')
            self.restore_state()
        return success
    
    def rotate_ccw(self):
        self.save_state()
        self.orientation = (self.orientation - 1) % 4
        success = not self.check_collision()
        if (not success):
            print(f'Couldn\'t rotate counter-clockwise')
            self.restore_state()
        return success

    def hard_drop(self):
        final = False
        while not final:
            move_success = self.move('down')
            final = not move_success

    def reset_position(self):
        self.orientation = self.spawn_orientation()
        self.center = self.spawn_position()

class IMino(Mino):
    colour = 'light blue'

    @staticmethod
    def spawn_position():
        return (1,5)

    @staticmethod
    def preview_positions():
        return [(0,0), (0,1), (0,2), (0,3)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block1 = self.offset_from_center((-1, -2))
            block2 = self.offset_from_center((-1, -1))
            block3 = self.offset_from_center((-1, 0))
            block4 = self.offset_from_center((-1, 1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((-2, 0))
            block2 = self.offset_from_center((-1, 0))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((1, 0))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((0, -2))
            block2 = self.offset_from_center((0, -1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((0, 1))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((-2, -1))
            block2 = self.offset_from_center((-1, -1))
            block3 = self.offset_from_center((0, -1))
            block4 = self.offset_from_center((1, -1))
        return [block1, block2, block3, block4]


class JMino(Mino):
    colour = 'blue'

    @staticmethod
    def spawn_position():
        return (0,4)

    @staticmethod
    def preview_positions():
        return [(0,0), (1,0), (1,1), (1,2)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block1 = self.offset_from_center((-1, -1))
            block2 = self.offset_from_center((0, -1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((0, 1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((-1, 0))
            block4 = self.offset_from_center((-1, 1))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((0, -1))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((0, 1))
            block4 = self.offset_from_center((1, 1))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((-1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((1, 0))
            block4 = self.offset_from_center((1, -1))
        return [block1, block2, block3, block4]

class LMino(Mino):
    colour = 'orange'

    @staticmethod
    def spawn_position():
        return (0,4)

    @staticmethod
    def preview_positions():
        return [(1,0), (1,1), (1,2), (0,2)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block1 = self.offset_from_center((-1, 1))
            block2 = self.offset_from_center((0, 1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((0, -1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((-1, 0))
            block4 = self.offset_from_center((1, 1))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((0, -1))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((0, 1))
            block4 = self.offset_from_center((1, -1))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((-1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((1, 0))
            block4 = self.offset_from_center((-1, -1))
        return [block1, block2, block3, block4]

class OMino(Mino):
    colour = 'yellow'

    @staticmethod
    def spawn_position():
        return (1,5)

    @staticmethod
    def preview_positions():
        return [(0,0), (1,0), (0,1), (1,1)]

    @property
    def block_positions(self):
        block1 = self.offset_from_center((-1, -1))
        block2 = self.offset_from_center((-1, 0))
        block3 = self.offset_from_center((0, -1))
        block4 = self.offset_from_center((0, 0))
        return [block1, block2, block3, block4]

        
class SMino(Mino):
    colour = 'green'
    @staticmethod
    def spawn_position():
        return (0,4)
    
    @staticmethod
    def preview_positions():
        return [(1,0), (1,1), (0,1), (0,2)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block1 = self.offset_from_center((0, -1))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((-1, 0))
            block4 = self.offset_from_center((-1, 1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((-1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((0, 1))
            block4 = self.offset_from_center((1, 1))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((1, -1))
            block2 = self.offset_from_center((1, 0))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((0, 1))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((-1, -1))
            block2 = self.offset_from_center((0, -1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((1, 0))
        return [block1, block2, block3, block4]

class TMino(Mino):
    colour = 'purple'

    @staticmethod
    def spawn_position():
        return (0,4)

    @staticmethod
    def preview_positions():
        return [(0,1), (1,0), (1,1), (1,2)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block2 = self.offset_from_center((-1, 0))
            block1 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((0, 1))
            block4 = self.offset_from_center((0, -1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((-1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((1, 0))
            block4 = self.offset_from_center((0, 1))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((0, -1))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((0, 1))
            block4 = self.offset_from_center((1, 0))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((-1, 0))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((1, 0))
            block4 = self.offset_from_center((0, -1))
        return [block1, block2, block3, block4]

class ZMino(Mino):
    colour = 'red'

    @staticmethod
    def spawn_position():
        return (0,4)

    @staticmethod
    def preview_positions():
        return [(0,0), (0,1), (1,1), (1,2)]

    @property
    def block_positions(self):
        if self.orientation == Mino.MINO_UP:
            block1 = self.offset_from_center((-1, -1))
            block2 = self.offset_from_center((-1, 0))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((0, 1))
        elif self.orientation == Mino.MINO_RIGHT:
            block1 = self.offset_from_center((-1, 1))
            block2 = self.offset_from_center((0, 1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((1, 0))
        elif self.orientation == Mino.MINO_DOWN:
            block1 = self.offset_from_center((0, -1))
            block2 = self.offset_from_center((0, 0))
            block3 = self.offset_from_center((1, 0))
            block4 = self.offset_from_center((1, 1))
        elif self.orientation == Mino.MINO_LEFT:
            block1 = self.offset_from_center((1, -1))
            block2 = self.offset_from_center((0, -1))
            block3 = self.offset_from_center((0, 0))
            block4 = self.offset_from_center((-1, 0))
        return [block1, block2, block3, block4]

def create_mino(type, board):
    type = type.upper()
    match(type):
        case 'I':
            mino = IMino.spawn(board)
        case 'J':
            mino = JMino.spawn(board)
        case 'L':
            mino = LMino.spawn(board)
        case 'O':
            mino = OMino.spawn(board)
        case 'S':
            mino = SMino.spawn(board)
        case 'T':
            mino = TMino.spawn(board)
        case 'Z':
            mino = ZMino.spawn(board)
    return mino

def main():
    m = create_mino('i')
    print(m.block_positions)

if __name__ == '__main__':
    main()
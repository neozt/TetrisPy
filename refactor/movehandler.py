from copy import copy

import mino as mn
import board as bd
from mino import Mino
from board import Board
from position import Position

def is_valid_position(mino: Mino, board: Board):
    # Check to ensure that none of the mino's blocks are outside playing area or in an occupied cell
    for block in mino.blocks:
        # Check if it's inside the board
        within_horizontal_area = 0 <= block.x < bd.COLUMNS
        within_vertical_area = 0 <= block.y < bd.ROWS + 1
        if not within_horizontal_area or not within_vertical_area:
            return False
        # Check if it's not on an occupied cell
        if board.is_cell_occupied(block):
            return False

    return True

def do_if_valid(fn):
    # Decorator to save position of mino before performing move 
    # And restores the mino back to the original position if the move results in an invalid mino position
    # Returns if the move was successful or not
    def wrapfn(*args, **kwargs):
        mino = args[1]
        board = args[2]
        original_center = copy(mino.center)
        original_orientation = copy(mino.orientation)
        fn(*args, **kwargs)

        valid = is_valid_position(mino, board)
        if not valid:
            mino.center = original_center
            mino.orientation = original_orientation
        return valid
            
    return wrapfn

class MoveHandler:
    @do_if_valid
    def move_mino_left(self, mino: Mino, board: Board):
        mino.left()

    @do_if_valid
    def move_mino_right(self, mino: Mino, board: Board):
        mino.right()

    @do_if_valid
    def move_mino_down(self, mino: Mino, board: Board):
        mino.down()

    def hard_drop_mino(self, mino: Mino, board: Board):
        dropped = self.move_mino_down(mino, board)
        while (dropped):
            dropped = self.move_mino_down(mino, board)


def test():
    mover = MoveHandler()
    mino = mn.create_mino('Z')
    board = Board()
    print(mino)
    mover.move_mino_left(mino, board)
    mover.hard_drop_mino(mino, board)
    print(mino)
    print(mino.blocks)



if __name__ == '__main__':
    test()

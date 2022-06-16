from copy import copy

import mino as mn
import board as bd
from mino import Mino, Orientation
from board import Board
from position import Position
from kicktable import KickTable
from movetype import MoveType


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


def undo_if_invalid(fn):
    # Decorator to save position of mino before performing move
    # And restores the mino back to the original position if the move results in an invalid mino position
    # If the move was successfuly, set the move as the movehandler's recent_move_executed and return True
    def wrappedfn(*args, **kwargs) -> bool:
        movehandler: PieceMovement = args[0]
        mino: Mino = args[1]
        board: Board = args[2]
        original_center = copy(mino.center)
        original_orientation = copy(mino.orientation)
        move_type = fn(*args, **kwargs)

        success = is_valid_position(mino, board)
        if success:
            movehandler.recent_move_executed = move_type
        else:
            mino.center = original_center
            mino.orientation = original_orientation
        return success

    return wrappedfn


class PieceMovement:
    def __init__(self, kick_table: KickTable = KickTable()) -> None:
        self.kick_table: KickTable = kick_table
        self.recent_move_executed: MoveType = None

    @ undo_if_invalid
    def move_left(self, mino: Mino, board: Board) -> MoveType:
        mino.left()
        return MoveType.LEFT

    @ undo_if_invalid
    def move_right(self, mino: Mino, board: Board) -> MoveType:
        mino.right()
        return MoveType.RIGHT

    @ undo_if_invalid
    def move_down(self, mino: Mino, board: Board) -> MoveType:
        mino.down()
        return MoveType.DOWN

    def hard_drop(self, mino: Mino, board: Board) -> None:
        # Move mino down until no longer possible
        dropped = self.move_down(mino, board)
        while (dropped):
            dropped = self.move_down(mino, board)

    def rotate_cw(self, mino: Mino, board: Board) -> bool:
        return self.rotate_with_kicks(mino, board, 'cw')

    def rotate_ccw(self, mino: Mino, board: Board) -> bool:
        return self.rotate_with_kicks(mino, board, 'ccw')

    def rotate_with_kicks(self, mino: Mino, board: Board, direction: str) -> bool:
        current_orientation: Orientation = mino.orientation
        target_orientation: Orientation = current_orientation.clockwise(
        ) if direction == 'cw' else current_orientation.counterclockwise()

        # Try each kicks in the kick table in sequence until the first valid kick is found
        kicks = self.kick_table.get_kicks(
            current_orientation.value, target_orientation.value, mino.type)
        for kick in kicks:
            success = self.rotate_with_kick(mino, board, direction, kick)
            if success:
                break
        return success

    @ undo_if_invalid
    def rotate_with_kick(self, mino: Mino, board: Board, direction: str, offset: tuple[int, int]) -> MoveType:
        # Rotates based on direction
        if direction == 'cw':
            mino.rotate_cw()
            rotate_type = MoveType.ROTATE_CW
        elif direction == 'ccw':
            mino.rotate_ccw()
            rotate_type = MoveType.ROTATE_CCW

        # "Kick" the mino by translating based on the offset
        mino.translate(offset)
        return rotate_type


def test():
    mover = PieceMovement()
    mino = mn.create_mino('Z')
    board = Board()
    print(mino)
    board.set_cell_colour(Position(3, 19), 'red')
    board.set_cell_colour(Position(5, 19), 'red')
    board.set_cell_colour(Position(4, 16), 'red')

    def rotate_and_print():
        print(mover.rotate_cw(mino, board))
        print(mino)
        print(mino.blocks)

    rotate_and_print()


if __name__ == '__main__':
    # test()
    pass

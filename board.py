from position import Position
from lineclear import LineClear
from mino import Mino
from movetype import MoveType

ROWS = 20
COLUMNS = 10
EMPTY = 'grey'
EMPTY_ROW = [EMPTY for x in range(COLUMNS)]


class Board:
    """
    Class that holds board state in a 10 by 20 array.
    (0,0) denotes the bottom left corner, (10,20) denotes the top right corner.
    The elements in the array represents the colour of the corresponding cell.
    """

    def __init__(self) -> None:
        self.board_arr = list()
        init_board(self.board_arr)

    def __str__(self) -> str:
        divider = '-' * 82
        board = ''
        for row in reversed(self.board_arr):
            board += '|'
            for cell in row:
                board += cell.center(12)
            board += '|' + '\n'
        return divider + '\n' + board + divider

    @property
    def rows(self) -> int:
        return ROWS

    @property
    def columns(self) -> int:
        return COLUMNS

    def set_cell_colour(self, cell: Position, colour: str) -> None:
        try:
            self.board_arr[cell.y][cell.x] = colour
        except IndexError:
            raise ValueError(
                f'Cell should be within (0,0) -> ({ROWS-1},{COLUMNS-1})')

    def get_cell_colour(self, cell: Position) -> None:
        try:
            return self.board_arr[cell.y][cell.x]
        except IndexError:
            raise ValueError(
                f'Cell should be within (0,0) -> ({ROWS-1},{COLUMNS-1})')

    def is_cell_occupied(self, cell: Position) -> bool:
        if not 0 <= cell.x < COLUMNS or not 0 <= cell.y < ROWS:
            return False
        return not is_empty(self.get_cell_colour(cell))


class BoardManager:
    """
    Class to manage higher level board operations such as finding cleared lines and
    performing line clears.
    """

    def __init__(self, board: Board) -> None:
        self.board = board

    def find_and_clear_lines(self, mino: Mino, previous_move: MoveType) -> LineClear | None:
        filled_lines = self.find_filled_lines()
        if filled_lines:
            tspin = self.detect_tspin(mino, previous_move)
            num_lines_cleared = len(filled_lines)
            self.clear_lines(filled_lines)
            return LineClear(num_lines_cleared, tspin)

        return None

    def detect_tspin(self, mino: Mino, previous_move: MoveType) -> bool:
        # Returns true if the line clear was a t spin
        # Three criteria for a line clear to be considered a T-spin:
        # 1. The mino placed causing the line clear should be a TMino
        # 2. The last move before the TMino was placed should be a rotation
        # 3. 3-4 corners of the center of the TMino should be occupied
        #    (either by solid blocks or walls/floors of the board)
        if mino.type != 'T':
            return False

        if not previous_move.is_rotation():
            return False

        corners = get_corners(mino.center)
        occupied_corners = 0
        for corner in corners:
            if (is_occupied(corner, self.board)):
                occupied_corners += 1
        return occupied_corners >= 3

    def find_filled_lines(self) -> list[int]:
        cleared_lines = []
        for i, row in enumerate(self.board.board_arr):
            if is_row_filled(row):
                cleared_lines.append(i)
        return cleared_lines

    def clear_lines(self, lines: list[int]) -> None:
        for line_no in sorted(lines, reverse=True):
            self.remove_row(line_no)
        for _ in range(len(lines)):
            self.add_row()

    def remove_row(self, row: int) -> None:
        self.board.board_arr.pop(row)

    def add_row(self) -> None:
        add_empty_row(self.board.board_arr)

    def add_mino(self, mino: Mino) -> None:
        for block in mino.blocks:
            self.board.set_cell_colour(block, mino.colour)


def get_corners(position: Position) -> list[Position]:
    corners = []
    offsets = [
        Position(-1, 1),
        Position(-1, -1),
        Position(1, 1),
        Position(1, -1)
    ]
    for offset in offsets:
        corners.append(position + offset)
    return corners


def is_occupied(position: Position, board: Board):
    # For t spin detection, the walls and floor of board counts as filled blocks
    if position.x < 0 or position.x >= 10:
        return True
    if position.y < 0:
        return True

    return board.is_cell_occupied(position)


def init_board(board):
    for _ in range(ROWS):
        add_empty_row(board)


def add_empty_row(board):
    board.append(EMPTY_ROW.copy())


def is_empty(val) -> bool:
    return val == EMPTY


def is_row_filled(row) -> bool:
    for cell in row:
        if is_empty(cell):
            return False
    return True


def test():
    board = Board()
    board.set_cell_colour(Position(0, 0), 'red')
    board.set_cell_colour(Position(9, 2), 'green')
    board.set_cell_colour(Position(9, 19), 'green')
    a = board.get_cell_colour(Position(0, 0))
    b = board.get_cell_colour(Position(0, 11))
    print(board)
    for i in range(COLUMNS):
        cell = Position(i, 1)
        board.set_cell_colour(cell, 'yellow')
        cell = Position(i, 5)
        board.set_cell_colour(cell, 'yellow')
        cell = Position(i, 10)
        board.set_cell_colour(cell, 'yellow')
    print(board)
    bm = BoardManager(board)
    print(cl := bm.find_filled_lines())
    bm.clear_lines(cl)
    print(board)


if __name__ == '__main__':
    test()

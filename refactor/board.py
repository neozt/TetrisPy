from position import Block

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
                board += cell.center(8)
            board += '|' + '\n'
        return divider + '\n' + board + divider

    def set_cell_colour(self, cell: Block, colour: str) -> None:
        try:
            self.board_arr[cell.y][cell.x] = colour
        except IndexError:
            raise ValueError(f'Cell should be within (0,0) -> ({ROWS-1},{COLUMNS-1})')
            
    def get_cell_colour(self, cell: Block) -> None:
        try:
            return self.board_arr[cell.y][cell.x]
        except IndexError:
            raise ValueError(f'Cell should be within (0,0) -> ({ROWS-1},{COLUMNS-1})')

    def is_cell_occupied(self, cell: Block) -> bool:
        if not 0 <= cell.x <= COLUMNS or not 0 <= cell.y <= ROWS: 
            return False
        return not is_empty(self.get_cell_colour(cell))



class BoardManager:
    """
    Class to manage higher level board operations such as finding cleared lines and 
    performing line clears.
    """
    def __init__(self, board: Board) -> None:
        self.board = board

    def find_cleared_lines(self) -> list[int]:
        cleared_lines = []
        for i, row in enumerate(self.board.board_arr):
            if is_row_filled(row):
                cleared_lines.append(i)
        return cleared_lines

    def clear_lines(self, lines: list[int]) -> None:
        for line_no in sorted(lines, reverse = True):
            self.remove_row(line_no)
        for _ in range(len(lines)):    
            self.add_row()

    def remove_row(self, row: int) -> None:
        self.board.board_arr.pop(row)

    def add_row(self) -> None:
        add_empty_row(self.board.board_arr)



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
    board.set_cell_colour(Block(0,0), 'red')
    board.set_cell_colour(Block(9,2), 'green')
    board.set_cell_colour(Block(9,19), 'green')
    a = board.get_cell_colour(Block(0,0))
    b = board.get_cell_colour(Block(0,11))
    print(board)
    for i in range(COLUMNS):
        cell = Block(i, 1)
        board.set_cell_colour(cell, 'yellow')
        cell = Block(i, 5)
        board.set_cell_colour(cell, 'yellow')
        cell = Block(i, 10)
        board.set_cell_colour(cell, 'yellow')
    print(board)
    bm = BoardManager(board)
    print(cl := bm.find_cleared_lines())
    bm.clear_lines(cl)
    print(board)

if __name__ == '__main__':
    test()

from asyncio.proactor_events import _ProactorDuplexPipeTransport


class Board:
    ROWS = 20
    COLUMNS = 10
    EMPTY = 'grey'

    def __init__(self):
        self.board = list()
        self.init_empty_board()

    def __repr__(self):
        string = '\n'.join([repr(row) for row in self.board])
        return string

    def init_empty_board(self):
        for y in range(Board.ROWS):
            self.add_empty_row()

    def add_empty_row(self):
        self.board.insert(0, [Board.EMPTY for x in range(Board.COLUMNS)])

    def set_cell_colour(self, coords, colour):
        self.board[coords[0]][coords[1]] = colour

    def get_cell_colour(self, coords):
        return self.board[coords[0]][coords[1]]

    def is_occupied(self, coords):
        if not 0 <= coords[0] <= Board.ROWS or not 0 <= coords[1] <= Board.COLUMNS: 
            return False
        return self.get_cell_colour(coords) != Board.EMPTY

    def is_empty(self, cell):
        return cell == Board.EMPTY

    def add_mino_to_board(self, mino):
        blocks = mino.block_positions
        for block in blocks:
            self.set_cell_colour(block, mino.colour)

    def find_cleared_lines(self):
        cleared_lines = list()
        for i, row in enumerate(self.board):
            if self.is_row_filled(row):
                cleared_lines.append(i)
        return cleared_lines

    def is_row_filled(self, row):
        for cell in row:
            if self.is_empty(cell):
                return False
        return True

    def clear_lines(self, lines):
        print(f'{lines}:\n{self}')
        for line_no in sorted(lines, reverse = True):
            self.board.pop(line_no)
        for i in range(len(lines)):    
            self.add_empty_row()

def test():
    board = Board()
    for i in range(10):
        board.board[17][i] = 'purple'
        board.board[16][i] = 'red'

    print(board)
    print(a:=board.find_cleared_lines())
    board.clear_lines(a)
    print(a)
    print(board)

if __name__ == '__main__':
    test()

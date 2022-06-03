import pygame

class Renderer:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 700
    FRAMERATE = 60
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

    def render_game(self):
        self.draw_board()
        self.draw_mino()

    def draw_board(self):
        board_cells = pygame.sprite.Group()
        for row in range(self.game.board.ROWS):
            for col in range(self.game.board.COLUMNS):
                cell = CellSurface((row,col), self.game.board.get_cell_colour((row,col)))
                board_cells.add(cell)
        for cell in board_cells:
            self.screen.blit(cell.surf, cell.coords)

    def draw_mino(self):
        mino_cells = pygame.sprite.Group()
        blocks = self.game.mino.block_positions
        for x, y in blocks:
            block = CellSurface((x, y), self.game.mino.colour)
            mino_cells.add(block)
        for cell in mino_cells:
            self.screen.blit(cell.surf, cell.coords)

    def line_clear_animation(self, cleared_lines):
        pass

class CellSurface(pygame.sprite.Sprite):
    CELL_LENGTH = 30

    def __init__(self, coords, colour):
        super(CellSurface, self).__init__()
        self.surf = pygame.Surface((CellSurface.CELL_LENGTH, CellSurface.CELL_LENGTH))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()
        self.coords = CellSurface.board_to_pixel_coords(coords, CellSurface.CELL_LENGTH)

    @staticmethod
    def board_to_pixel_coords(coords, length):
        y, x= coords
        return (x * length, y * length)
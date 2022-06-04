import pygame

class Renderer:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FRAMERATE = 60
    BAORD_ORIGIN = (150, 20)

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

    def render_game(self):
        self.screen.fill((255, 255, 255))
        self.draw_board()
        self.draw_mino()
        self.draw_previews()

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
    
    def draw_previews(self):
        preview_cells = pygame.sprite.Group()
        preview_pieces = self.game.queue.peek(5)
        for i, piece in enumerate(preview_pieces):
            piece_cells = piece.preview_positions()
            for cell in piece_cells:
                block = PreviewCellSurface(cell, i, piece.colour)
                preview_cells.add(block)
        for cell in preview_cells:
            self.screen.blit(cell.surf, cell.coords)

    def line_clear_animation(self, cleared_lines):
        pass

class CellSurface(pygame.sprite.Sprite):
    CELL_LENGTH = 30
    BOARD_ORIGIN = (150,0)

    def __init__(self, coords, colour):
        super(CellSurface, self).__init__()
        self.surf = pygame.Surface((CellSurface.CELL_LENGTH, CellSurface.CELL_LENGTH))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()
        self.coords = CellSurface.board_to_pixel_coords(coords, CellSurface.CELL_LENGTH)

    @staticmethod
    def board_to_pixel_coords(coords, length):
        y, x = coords
        return (x * length + CellSurface.BOARD_ORIGIN[0],
                y * length + CellSurface.BOARD_ORIGIN[1])

class PreviewCellSurface(pygame.sprite.Sprite):
    CELL_LENGTH = 30
    PREVIEWER_ORIGIN = (550, 50)
    PREVIEW_GAP = 20

    def __init__(self, coords, preview_position, colour):
        super(PreviewCellSurface, self).__init__()
        self.surf = pygame.Surface((self.CELL_LENGTH, self.CELL_LENGTH))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()
        self.coords = self.get_preview_block_coords(coords, preview_position, self.CELL_LENGTH)

    @staticmethod
    def get_preview_block_coords(coords, preview_position, length):
        y, x = coords
        x_actual = x * length + PreviewCellSurface.PREVIEWER_ORIGIN[0]
        offset_from_top = preview_position * (PreviewCellSurface.CELL_LENGTH * 2 + PreviewCellSurface.PREVIEW_GAP)
        y_actual = y * length + PreviewCellSurface.PREVIEWER_ORIGIN[1] + offset_from_top
        return (x_actual, y_actual)   
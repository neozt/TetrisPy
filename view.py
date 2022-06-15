from game import Game, EventType
from board import Board
from pieceholder import Hold
import mino as mn
from mino import Mino

import pygame
from pygame.locals import *
from piecequeue import PieceQueue

from position import Position

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BOARD_POSITION = (200, 20)
HOLDER_POSITION = (70, 50)
HOLDER_CELLS = (4, 2)
PREVIEW_POSITION = (550, 50)
PREVIEW_CELLS = (4, 2)
PREVIEW_MARGIN = 15
CELL_WIDTH = 30


def normalised_position_to_holder_position(cell: Position):
    return cell + Position(1, 0)


class RectangleSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str):
        super(RectangleSprite, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = pygame.Rect(x, y, width, height)


class View:
    def __init__(self):
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, game: Game, update_type: EventType = EventType.NORMAL):
        if update_type == EventType.LINE_CLEAR:
            self.render_line_clear(game)
        elif update_type == EventType.DEATH:
            self.render_death(game)

        self.render_game(game)

    def render_game(self, game: Game):
        self.surface.fill('black')
        self.draw_board(game.board)
        self.draw_hold(game.hold)
        self.draw_previews(game.queue)
        self.draw_mino(game.current_mino)
        pygame.display.flip()

    def draw_mino(self, mino: Mino):
        mino_sprite = pygame.sprite.Group()
        for block in mino.blocks:
            x = BOARD_POSITION[0] + block.x * CELL_WIDTH
            y = BOARD_POSITION[1] + (19 - block.y) * CELL_WIDTH
            if y < BOARD_POSITION[1]:
                continue    # Don't draw block if higher than top of board

            mino_sprite.add(RectangleSprite(
                x, y, CELL_WIDTH, CELL_WIDTH, mino.colour
            ))
        mino_sprite.draw(self.surface)

    def draw_board(self, board: Board):
        board_sprite = pygame.sprite.Group()
        for row in range(board.rows):
            for column in range(board.columns):
                x = BOARD_POSITION[0] + column * CELL_WIDTH
                y = BOARD_POSITION[1] + row * CELL_WIDTH
                # Since tetris board positive-y is opposite to pygame's positive-y,
                # we invert the y position to get the actual colour
                pos = Position(column, board.rows - row - 1)
                colour = board.get_cell_colour(pos)
                board_sprite.add(RectangleSprite(
                    x, y, CELL_WIDTH, CELL_WIDTH, colour))
        board_sprite.draw(self.surface)

    def draw_hold(self, hold: Hold):
        holder_sprite = pygame.sprite.Group()

        mino = hold.held_mino
        if mino is not None:
            blocks = [normalised_position_to_holder_position(
                block) for block in mino.normalised_positions]
            colour = mino.colour
        else:
            blocks = []
            colour = 'grey'

        for block in blocks:
            x = block.x * CELL_WIDTH + HOLDER_POSITION[0]
            y = (HOLDER_CELLS[1] - block.y) * CELL_WIDTH + HOLDER_POSITION[1]
            holder_sprite.add(RectangleSprite(
                x, y, CELL_WIDTH, CELL_WIDTH, colour
            ))
        holder_sprite.draw(self.surface)

    def draw_previews(self, queue: PieceQueue):
        preview_pieces = queue.peek(5)
        for i, piece in enumerate(preview_pieces):
            self.draw_preview(i, piece)

    def draw_preview(self, i: int, piece: Mino):
        preview_sprite = pygame.sprite.Group()
        blocks = [normalised_position_to_holder_position(
            block) for block in piece.normalised_positions]
        for block in blocks:
            x = block.x * CELL_WIDTH + PREVIEW_POSITION[0]
            # offset due to preceeding preview pieces
            vertical_offset = i * PREVIEW_CELLS[1]\
                * (CELL_WIDTH+PREVIEW_MARGIN)
            y = (PREVIEW_CELLS[1]-block.y)*CELL_WIDTH\
                + PREVIEW_POSITION[1] + vertical_offset
            preview_sprite.add(
                RectangleSprite(x, y, CELL_WIDTH, CELL_WIDTH, piece.colour)
            )
        preview_sprite.draw(self.surface)

    def render_line_clear(self, game: Game):
        print(f'Line cleared: {game.previous_line_clear.abbreviation}')
        print(f'Current score: {game.current_score}')
        print(f'History {game.line_clears}')

    def render_death(self, game: Game):
        print("GAME OVER")


def test():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game()
    view = View(surface)
    view.update(game)
    pygame.display.flip()
    running = True
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False


if __name__ == '__main__':
    test()

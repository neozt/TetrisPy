import pygame
from piecequeue import PieceQueue
from mino import Mino
from board import Board
from renderer import Renderer
from movehandler import MovementHandler
from hold import Hold

class Game:
    SOFT_DROP_MULTIPLIER = 4

    def __init__(self, gravity = 30):
        self.board = Board()
        self.queue = PieceQueue(self.board)
        self.mino = self.queue.pop()
        self.mino_holder = Hold(self)
        self.move_handler = MovementHandler(self)
        self.running = True
        self.gravity = gravity     # Number of frames to wait before mino move down 1 block
        self.double_gravity = self.gravity // Game.SOFT_DROP_MULTIPLIER
        self.soft_dropping = False
        self.tick_counter = 0

    def handle_gravity(self):
        self.move_handler.handle_gravity()

    def check_and_handle_line_clears(self):
        cleared_lines = self.board.find_cleared_lines()
        if cleared_lines:
            self.board.clear_lines(cleared_lines)
        return cleared_lines

    def stop_game(self):
        print("Game over")
        self.running = False

    def check_death(self):
        # Death occurs when mino is in an occupied position
        # This will happen only during spawning
        death = self.mino.check_collision()
        return death

    def move_mino_left(self):
        self.mino.move('left')

    def move_mino_right(self):
        self.mino.move('right')

    def move_mino_down(self):
        self.mino.move('down')

    def rotate_mino_cw(self):
        self.mino.rotate_cw()

    def rotate_mino_ccw(self):
        self.mino.rotate_ccw()        

    def rotate_mino_180(self):
        pass

    def harddrop_mino(self):
        self.mino.hard_drop()
        self.board.add_mino_to_board(self.mino)
        self.get_next_mino()
        self.mino_holder.enable_hold()

    def softdrop_mino(self):
        self.mino.move('down')

    def hold(self):
        try:
            new_mino = self.mino_holder.hold_mino(self.mino)
            if new_mino is not None:
                self.mino = new_mino
            else:
                self.get_next_mino()
            self.mino_holder.disable_hold()
        except Exception as e:
            pass

    def get_next_mino(self):
        self.mino = self.queue.pop()

    def perform_moves(self):
        for move, count in self.move_handler.move_count.items():
            for i in range(count):
                self.perform_move(move)

    def perform_move(self, move):
        match(move):
            case 'left':
                self.move_mino_left()
            case 'right':
                self.move_mino_right()
            case 'rotatecw':
                self.rotate_mino_cw()
            case 'rotateccw':
                self.rotate_mino_ccw()
            case 'rotate180':
                self.rotate_mino_180()
            case 'down':
                self.softdrop_mino()
            case 'harddrop':
                self.harddrop_mino()
            case 'hold':
                self.hold()
    

    def process_inputs(self, keys):
        self.move_handler.process_inputs(keys)

    def tick(self):
        self.move_handler.tick()


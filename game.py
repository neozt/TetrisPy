from mino import Mino
from board import Board, BoardManager
from pieceholder import Hold, NoHeldMinoException
from piecequeue import PieceQueue
from piecemovement import PieceMovement

from dataclasses import dataclass, asdict

@dataclass
class GameInput:
    left: int = 0
    right: int = 0
    rotate_cw: int = 0
    rotate_ccw: int = 0
    rotate_180: int = 0
    soft_drop: bool = False
    hard_drop: bool = False
    hold: bool = False

class Game:
    def __init__(self, gravity = 30):
        self.board: Board = Board()
        self.board_manager: BoardManager = BoardManager(self.board)
        self.hold: Hold = Hold()
        self.queue: PieceQueue = PieceQueue()
        self.move_handler: PieceMovement = PieceMovement()
        self.ticks_since_last_drop = 0
        self.gravity = gravity

    def update(self, input: GameInput):
        # Handle user input
        self.perform_user_movements(input)
        # Handle vertical movement
        self.handle_vertical_movement(input)
        # Handle line clears
        self.handle_line_clears()
        # Handle death

    def handle_line_clears(self):
        cleared_lines = self.board_manager.find_cleared_lines()


    def perform_user_movements(self, input: GameInput):
        """Handle user inputs for horizontal movement, holding, and rotation"""
        for key, value in asdict(input).items():
            self.perform_move(key, value)

    def perform_move(self, input_type: str, value: int | bool) -> None:
        match input_type:
            case 'left':
                for _ in range(value):
                    self.move_handler.move_left(self.mino, self.board)
            case 'right':
                for _ in range(value):
                    self.move_handler.move_right(self.mino, self.board)
            case 'rotate_cw':
                for _ in range(value):
                    self.move_handler.rotate_cw(self.mino, self.board)
            case 'rotate_ccw':
                for _ in range(value):
                    self.move_handler.rotate_ccw(self.mino, self.board)
            case 'hold':
                if value:
                    self.hold_mino()

    def hold_mino(self):
        try: 
            previously_held: Mino = self.hold.hold_mino(self.mino)
            if previously_held is None:
                self.spawn_mino()
            else:
                self.mino = previously_held

        except NoHeldMinoException:
            pass

    def spawn_mino(self):
        self.mino = self.queue.pop()

    def handle_vertical_movement(self, input: GameInput) -> None:
        if input.hard_drop:
            self.hard_drop()
        elif input.soft_drop:
            self.drop()
        else:
            # Handle gravity
            self.ticks_since_last_drop += 1
            if self.gravity_pulls():
                self.drop()

    def hard_drop(self) -> None:
        self.move_handler.hard_drop(self.mino, self.board)
        self.spawn_mino()
        self.reset_gravity_ticks()

    def drop(self) -> None:
        self.move_handler.move_down(self.mino, self.board)
        self.reset_gravity_ticks()
    
    def reset_gravity_ticks(self) -> None:
        self.ticks_since_last_drop = 0

    def gravity_pulls(self) -> bool:
        return self.ticks_since_last_drop > self.gravity
            

def test():
    a = GameInput()
    for key, value in asdict(a).items():
        print(key)
        print(value)

if __name__ == '__main__':
    test()
from mino import Mino
from board import Board, BoardManager
from pieceholder import Hold, NoHeldMinoException
from piecequeue import PieceQueue
from piecemovement import PieceMovement
from lineclear import LineClear

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
        self.queue: PieceQueue = PieceQueue()
        self.hold: Hold = Hold()
        self.move_handler: PieceMovement = PieceMovement()
        self.current_mino: Mino = self.spawn_mino()
        self.previous_mino: Mino = None

        self.alive = True
        self.ticks_since_last_drop = 0
        self.gravity = gravity

        self.total_clears: list[LineClear] = []

        self.observers = []

    def update(self, input: GameInput):
        # Handle user input
        self.perform_user_movements(input)
        # Handle vertical movement
        self.handle_vertical_movement(input)
        # Handle line clears
        self.board_manager.find_and_clear_lines(self.current_mino)
        # Handle death
        self.check_and_handle_death()

    def handle_line_clears(self):
        # Check if there are any lines that need to be cleared
        line_clear = self.board_manager.find_and_clear_lines(self.previous_mino) 
        
        if line_clear is not None:
            self.append_line_clear(line_clear)
            self.notify_line_clear_observers()

    def perform_user_movements(self, input: GameInput):
        """Handle user inputs for horizontal movement, holding, and rotation"""
        for key, value in asdict(input).items():
            self.perform_move(key, value)

    def perform_move(self, input_type: str, value: int | bool) -> None:
        requires_update = False
        match input_type:
            case 'left':
                for _ in range(value):
                    requires_update = self.move_handler.move_left(self.current_mino, self.board)
            case 'right':
                for _ in range(value):
                    requires_update = self.move_handler.move_right(self.current_mino, self.board)
            case 'rotate_cw':
                for _ in range(value):
                    requires_update = self.move_handler.rotate_cw(self.current_mino, self.board)
            case 'rotate_ccw':
                for _ in range(value):
                    requires_update = self.move_handler.rotate_ccw(self.current_mino, self.board)
            case 'hold':
                if value:
                    requires_update = self.hold_mino()
        
        if requires_update:
            self.notify_observers()

    def hold_mino(self) -> bool:
        try: 
            previously_held = self.hold.hold_mino(self.current_mino)
        except NoHeldMinoException:
            return False

        if previously_held is None:
            self.spawn_mino()
        else:
            self.current_mino = previously_held
        return True

    def spawn_mino(self) -> Mino:
        return self.queue.pop()

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
        self.move_handler.hard_drop(self.current_mino, self.board) # Move mino to bottom
        self.board_manager.add_mino(self.current_mino) # Mino becomes part of board now
        self.previous_mino = self.current_mino  # Mino is no longer current
        self.current_mino = self.spawn_mino()   # Spawn new mino
        self.reset_gravity_ticks()
        self.notify_observers()

    def drop(self) -> None:
        self.move_handler.move_down(self.current_mino, self.board)
        self.reset_gravity_ticks()
        self.notify_observers()
    
    def reset_gravity_ticks(self) -> None:
        self.ticks_since_last_drop = 0

    def gravity_pulls(self) -> bool:
        return self.ticks_since_last_drop > self.gravity

    def check_and_handle_death(self):
        dead = self.check_death()
        if dead:
            self.notify_death_observers()
            self.stop()

    def check_death(self):
        for block in self.current_mino.blocks:
            if self.board.is_cell_occupied(block):
                return True
        return False

    def stop(self):
        self.alive = False

    @property
    def current_score(self) -> int:
        return sum([clear.score for clear in self.total_clears])

    def append_line_clear(self, line_clear: LineClear) -> None:
        self.total_clears.append(line_clear)

    def register_observer(self, observer) -> None:
        self.observers.append(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update(self)

    def notify_line_clear_observers(self) -> None:
        for observer in self.observers:
            observer.update(self, 'line clear')

    def notify_death_observers(self) -> None:
        for observer in self.observers:
            observer.update(self, 'death')



def test():
    a = GameInput()
    for key, value in asdict(a).items():
        print(key)
        print(value)

if __name__ == '__main__':
    test()
import copy
from dataclasses import dataclass, asdict
from enum import Enum, auto

from mino import Mino
from board import Board, BoardManager
from pieceholder import Hold, HoldDisabledException
from piecequeue import PieceQueue
from piecemovement import PieceMovement
from lineclear import LineClear
from inputs import GameInput


class EventType(Enum):
    NORMAL = auto()
    LINE_CLEAR = auto()
    DEATH = auto()


def default_history_dict() -> dict[LineClear, int]:
    return {
        LineClear(1, False): 0,
        LineClear(2, False): 0,
        LineClear(3, False): 0,
        LineClear(4, False): 0,
        LineClear(1, True): 0,
        LineClear(2, True): 0,
        LineClear(3, True): 0
    }


class Game:
    def __init__(self, gravity=30):
        self.observers = []
        self.gravity = gravity

    def start(self):
        self.board: Board = Board()
        self.board_manager: BoardManager = BoardManager(self.board)
        self.queue: PieceQueue = PieceQueue()
        self.hold: Hold = Hold()

        self.move_handler: PieceMovement = PieceMovement()
        # move_handler.hard_drop() is invoked when generating shadow, so we use a
        # seperate instance to not affect normal movement (since move_handler) needs to keep
        # track of previous movement for tspin detection
        self.shadow_move_handler: PieceMovement = PieceMovement()

        self.current_mino: Mino = self.queue.pop()
        self.previous_mino: Mino = None

        self.alive = True
        self.ticks_since_last_drop = 0

        self.previous_line_clear: LineClear = None
        self.line_clears: dict[LineClear, int] = default_history_dict()

        self.notify_observers()

    def reset(self):
        self.start()

    def update(self, input: GameInput):
        # Handle user input
        self.perform_user_movements(input)
        # Handle vertical movement
        self.handle_vertical_movement(input)
        # Handle line clears
        self.handle_line_clears()
        # Handle death
        self.check_and_handle_death()

    def handle_line_clears(self):
        # Check if there are any lines that need to be cleared
        line_clear = self.board_manager.find_and_clear_lines(
            self.previous_mino, self.move_handler.recent_move_executed)
        if line_clear is not None:
            self.add_line_clear(line_clear)
            self.notify_observers(EventType.LINE_CLEAR)

    def perform_user_movements(self, input: GameInput):
        """Handle user inputs for horizontal movement, holding, and rotation"""
        for key, value in asdict(input).items():
            self.perform_move(key, value)

    def perform_move(self, input_type: str, perform: bool) -> None:
        if perform == False:
            return

        requires_update = False
        match input_type:
            case 'move_left':
                success = self.move_handler.move_left(
                    self.current_mino, self.board)
                if success:
                    requires_update = True
            case 'move_right':
                success = self.move_handler.move_right(
                    self.current_mino, self.board)
                if success:
                    requires_update = True
            case 'rotate_cw':
                success = self.move_handler.rotate_cw(
                    self.current_mino, self.board)
                if success:
                    requires_update = True
            case 'rotate_ccw':
                success = self.move_handler.rotate_ccw(
                    self.current_mino, self.board)
                if success:
                    requires_update = True
            case 'rotate_180':
                success = self.move_handler.rotate_180(
                    self.current_mino, self.board)
                if success:
                    requires_update = True
            case 'hold':
                requires_update = self.hold_mino()

        if requires_update:
            self.notify_observers()

    def hold_mino(self) -> bool:
        try:
            previously_held = self.hold.hold_mino(self.current_mino)
        except HoldDisabledException:
            return False

        if previously_held is None:
            self.spawn_mino()
        else:
            self.current_mino = previously_held
        return True

    def spawn_mino(self) -> None:
        self.previous_mino = self.current_mino
        self.current_mino = self.queue.pop()

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
        self.add_mino_to_board()
        self.hold.enable_hold()
        self.reset_gravity_ticks()
        self.notify_observers()

    def add_mino_to_board(self) -> None:
        self.move_handler.hard_drop(
            self.current_mino, self.board)  # Move mino to bottom
        # Mino becomes part of board now
        self.board_manager.add_mino(self.current_mino)
        self.spawn_mino()   # Spawn new mino

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
            self.notify_observers(EventType.DEATH)
            self.end()

    def check_death(self):
        for block in self.current_mino.blocks:
            if self.board.is_cell_occupied(block):
                return True
        return False

    def end(self):
        self.alive = False

    def get_shadow(self):
        def fade_colour(colour: tuple[int, int, int]) -> tuple[int, int, int]:
            # return (169, 169, 169)
            return (int(colour[0]/3), int(colour[1]/3), int(colour[2]/3))

        # Create copy of current mino
        shadow = copy.copy(self.current_mino)
        # Set colour as a faded version of its original colour
        shadow.colour = fade_colour(shadow.colour)
        # Move shadow down as much as possible
        self.shadow_move_handler.hard_drop(shadow, self.board)
        return shadow

    @property
    def current_score(self) -> int:
        return sum(clear_type.score * count for clear_type, count in self.line_clears.items())

    def print_history(self) -> int:
        for lc, count in self.line_clears.items():
            print(f'{lc.abbreviation}: {count}')

    def add_line_clear(self, line_clear: LineClear) -> None:
        self.previous_line_clear = line_clear
        self.line_clears[line_clear] = self.line_clears.get(line_clear, 0) + 1

    def register_observer(self, observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, event: EventType = EventType.NORMAL) -> None:
        for observer in self.observers:
            observer.update(self, event)

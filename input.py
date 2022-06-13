from pygame.locals import *
from typing import ClassVar
from enum import Enum

from dataclasses import dataclass, field
from game import GameInput

MOVE_LEFT = K_LEFT
MOVE_RIGHT = K_RIGHT
ROTATE_CW = K_UP
ROTATE_CCW = K_z
ROTATE_180 = K_a
HOLD = K_c
SOFT_DROP = K_DOWN
HARD_DROP = K_SPACE

@dataclass
class UserInput:
    move_left: bool
    move_right: bool
    rotate_cw: bool
    rotate_ccw: bool
    rotate_180: bool
    hold: bool
    soft_drop: bool
    hard_drop: bool

    def __init__(self, inputs: dict[int, bool]):
        self.move_left = inputs.get(MOVE_LEFT, False)
        self.move_right = inputs.get(MOVE_RIGHT, False)
        self.rotate_cw = inputs.get(ROTATE_CW, False)
        self.rotate_ccw = inputs.get(ROTATE_CCW, False)
        self.rotate_180 = inputs.get(ROTATE_180, False)
        self.hold = inputs.get(HOLD, False)
        self.soft_drop = inputs.get(SOFT_DROP, False)
        self.hard_drop = inputs.get(HARD_DROP, False)
        

def require_auto_shift(ticks: int, arr: int, das: int) -> bool:
    # While a key is held, auto shift occurs every arr ticks, after an initial delay of das ticks between 
    # first movement due to key press and second movement due to auto shifting
    ticks = abs(ticks)
    if ticks <= das: 
        return False
    else:
        return ((ticks - das - 1) % arr ) == 0


@dataclass
class InputProcessor:
    """
    Translates user inputs to game inputs.
    Implements debounce, softdrop delays, and DAS and ARR for horizontal movement.
    """
    das: int = 10
    arr: int = 1
    softdrop_gravity: int = 5

    rotate_cw_held: bool = field(default = False, init = False)
    rotate_ccw_held: bool = field(default = False, init = False)
    hold_held: bool = field(default = False, init = False)
    harddrop_held: bool = field(default = False, init = False)
    softdrop_held_for: int = field(default = 0, init = False)
    horizontal_direction: int = field(default = 0, init = False)
    
    def process_inputs(self, inputs: UserInput) -> GameInput:
        left, right = self.handle_horizontal_inputs(inputs.move_left, inputs.move_right)
        rotate_cw, rotate_ccw, rotate_180 = self.handle_rotates(inputs.rotate_cw, inputs.rotate_ccw, inputs.rotate_180)
        hold = self.handle_hold(inputs.hold)
        soft_drop, hard_drop = self.handle_drops(inputs.soft_drop, inputs.hard_drop)
        
        return GameInput(left, right, rotate_cw, rotate_ccw, rotate_180, soft_drop, hard_drop, hold)


    def handle_horizontal_inputs(self, left_pressed: bool, right_pressed: bool) -> tuple[int, int]:
        if not left_pressed and not right_pressed:
            # Reset to neutral state
            self.horizontal_direction = 0
        left = right = 0
        if left_pressed:
            left = self.handle_left_input()
        if right_pressed:
            right = self.handle_right_input()
        return left, right

    def handle_left_input(self) -> int:
        # Piece was either in neutral position or moving right
        if self.horizontal_direction >= 0:
            self.horizontal_direction = -1
            return 1
        # Otherwise, we check if it is time for auto shift based on ARR and DAS
        else:
            self.horizontal_direction -= 1
            shift = require_auto_shift(
                self.horizontal_direction, self.arr, self.das)
            return 1 if shift else 0

    def handle_right_input(self) -> int:
        # Piece was either in neutral position or moving right
        if self.horizontal_direction <= 0:
            self.horizontal_direction = 1
            return 1
        # Otherwise, we check if it is time for auto shift based on ARR and DAS
        else:
            self.horizontal_direction += 1
            shift = require_auto_shift(
                self.horizontal_direction, self.arr, self.das)
            return 1 if shift else 0


    def handle_rotates(self, cw: bool, ccw: bool, hundred_eighty: bool) -> tuple[int, int, int]:
        clockwise = counterclockwise = hundred_eighty = 0
        if not cw: 
            self.rotate_cw_held = False
        else:
            # Rotate only if button isn't being held
            clockwise = 1 if not self.rotate_cw_held else 0
            self.rotate_cw_held = True

        if not ccw: 
            self.rotate_ccw_held = False
        else:
            counterclockwise = 1 if not self.rotate_ccw_held else 0
            self.rotate_ccw_held = True

        return clockwise, counterclockwise, hundred_eighty


    def handle_hold(self, hold: bool) -> int:
        should_hold = 0
        if not hold:
            self.hold_held = False
        else:
            should_hold = 1 if not self.hold_held else 0
            self.hold_held = True
        return should_hold


    def handle_drops(self, soft: bool, hard: bool) -> tuple[int, int]:
        softdrop = harddrop = 0
        if not soft:
            self.softdrop_held_for = 0
        else:
            softdrop = 1 if (self.softdrop_held_for % self.softdrop_gravity == 0) else  0
            self.softdrop_held_for += 1

        if not hard: 
            self.harddrop_held = False
        else:
            harddrop = 1 if not self.harddrop_held else 0
            self.harddrop_held = True

        return softdrop, harddrop

            
def test():
    processor = InputProcessor(
        das = 5,
        arr = 4
    )

    input = {
        MOVE_LEFT: False,
        MOVE_RIGHT: False,
        ROTATE_CW: False,
        ROTATE_180: False,
        ROTATE_CCW: False,
        HARD_DROP: False,
        SOFT_DROP: False,
        HOLD: False
    }

    softdrop = input.copy()
    softdrop[SOFT_DROP] = True

    harddrop = input.copy()
    harddrop[HARD_DROP] = True

    input = UserInput(input)
    softdrop = UserInput(softdrop)
    harddrop = UserInput(harddrop)

    def foo():
        print(processor.process_inputs(softdrop))
        # print(processor)
    def bar():
        print(processor.process_inputs(harddrop))

    def baz():
        print(processor.process_inputs(input))

    bar()
    bar()
    bar()
    bar()
    bar()
    print('here')
    baz()
    bar()
    baz()
    bar()
    baz()
    bar()




if __name__ == '__main__':
    test()




        

    

         
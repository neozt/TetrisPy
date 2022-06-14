import pygame
from pygame.locals import *
from typing import ClassVar
from enum import Enum

from dataclasses import dataclass, field

MOVE_LEFT = K_LEFT
MOVE_RIGHT = K_RIGHT
ROTATE_CW = K_UP
ROTATE_CCW = K_z
ROTATE_180 = K_a
HOLD = K_c
SOFT_DROP = K_DOWN
HARD_DROP = K_SPACE

@dataclass
class Input:
    move_left: bool = False
    move_right: bool = False
    rotate_cw: bool = False
    rotate_ccw: bool = False
    rotate_180: bool = False
    hold: bool = False
    soft_drop: bool = False
    hard_drop: bool = False

@dataclass
class GameInput(Input):
    pass

@dataclass
class UserInput(Input):
    def __init__(self, inputs: list[bool]):
        self.move_left = inputs[K_LEFT]
        self.move_right = inputs[K_RIGHT]
        self.rotate_cw = inputs[K_UP]
        self.rotate_ccw = inputs[K_z]
        self.rotate_180 = inputs[K_a]
        self.hold = inputs[K_c]
        self.soft_drop = inputs[K_DOWN]
        self.hard_drop = inputs[K_SPACE]
        

def require_auto_shift(ticks: int, arr: int, das: int) -> bool:
    # While a key is held, auto shift occurs every arr ticks, after an initial delay of das ticks between 
    # first movement due to key press and second movement due to auto shifting
    ticks = abs(ticks)
    if ticks <= das: 
        return False
    else:
        return ((ticks - das - 1) % arr ) == 0


def softdrop_interval_passed(ticks: int, interval_in_ticks: int) -> bool:
    return ticks % interval_in_ticks == 0


@dataclass
class InputProcessor:
    """
    Translates user inputs to game inputs.
    Implements debounce, softdrop delays, and DAS and ARR for horizontal movement.
    """
    das: int = 10
    arr: int = 1
    softdrop_gravity: int = 5

    # Variables to remember state
    rotate_cw_held: bool = field(default = False, init = False)
    rotate_ccw_held: bool = field(default = False, init = False)
    hold_held: bool = field(default = False, init = False)
    harddrop_held: bool = field(default = False, init = False)
    softdrop_held_for: int = field(default = 0, init = False)
    horizontal_direction: int = field(default = 0, init = False)
    
    def process_inputs(self, inputs: UserInput) -> GameInput:
        move_left, move_right = self.handle_horizontal_inputs(inputs.move_left, inputs.move_right)
        rotate_cw, rotate_ccw, rotate_180 = self.handle_rotates(inputs.rotate_cw, inputs.rotate_ccw, inputs.rotate_180)
        hold = self.handle_hold(inputs.hold)
        soft_drop, hard_drop = self.handle_drops(inputs.soft_drop, inputs.hard_drop)
        
        return GameInput(move_left, move_right, rotate_cw, rotate_ccw,rotate_180, hold, soft_drop, hard_drop)


    def handle_horizontal_inputs(self, left_pressed: bool, right_pressed: bool) -> tuple[bool, bool]:
        if not left_pressed and not right_pressed:
            # Reset to neutral state
            self.horizontal_direction = 0
        left = right = False
        if left_pressed:
            left = self.handle_left_input()
        if right_pressed:
            right = self.handle_right_input()
        return left, right

    def handle_left_input(self) -> bool:
        # Piece was either in neutral position or moving right
        if self.horizontal_direction >= 0:
            self.horizontal_direction = -1
            return True
        # Otherwise, we check if it is time for auto shift based on ARR and DAS
        else:
            self.horizontal_direction -= 1
            shift = require_auto_shift(
                self.horizontal_direction, self.arr, self.das)
            return shift

    def handle_right_input(self) -> bool:
        # Piece was either in neutral position or moving left
        if self.horizontal_direction <= 0:
            self.horizontal_direction = 1
            return True
        # Otherwise, we check if it is time for auto shift based on ARR and DAS
        else:
            self.horizontal_direction += 1
            shift = require_auto_shift(
                self.horizontal_direction, self.arr, self.das)
            return shift


    def handle_rotates(self, cw: bool, ccw: bool, hundred_eighty: bool) -> tuple[bool, bool, bool]:
        clockwise = counterclockwise = hundred_eighty = False
        if not cw: 
            self.rotate_cw_held = False
        else:
            # Rotate only if button isn't being held
            clockwise = not self.rotate_cw_held
            self.rotate_cw_held = True

        if not ccw: 
            self.rotate_ccw_held = False
        else:
            counterclockwise = not self.rotate_ccw_held
            self.rotate_ccw_held = True

        return clockwise, counterclockwise, hundred_eighty


    def handle_hold(self, hold: bool) -> bool:
        should_hold = False
        if not hold:
            self.hold_held = False
        else:
            should_hold = not self.hold_held
            self.hold_held = True
        return should_hold


    def handle_drops(self, soft: bool, hard: bool) -> tuple[bool, bool]:
        softdrop = harddrop = False
        if not soft:
            self.softdrop_held_for = 0
        else:
            softdrop = softdrop_interval_passed(self.softdrop_held_for, self.softdrop_gravity) 
            self.softdrop_held_for += 1

        if not hard: 
            self.harddrop_held = False
        else:
            harddrop = not self.harddrop_held
            self.harddrop_held = True

        return softdrop, harddrop



def test():

    # print(UserInput(inputs))
    return


if __name__ == '__main__':
    test()




        

    

         
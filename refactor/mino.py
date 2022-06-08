from abc import ABC, abstractproperty
from dataclasses import dataclass
from enum import Enum

from position import Position, GridPosition

class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

ROTATIONS_REQUIRED = {
    Orientation.UP: 0,
    Orientation.RIGHT: 1,
    Orientation.DOWN: 2,
    Orientation.LEFT: 3
}

@dataclass
class Mino(ABC):
    center: Position | GridPosition
    orientation: Orientation = Orientation.UP

    @abstractproperty
    def normalised_positions(self):
        pass

    @property
    def blocks(self) -> list[Position]:
        # Returns the position of the four mino blocks based on its current orientation and center
        # This default inherited method is used by LJZST minos.
        # O and I Minos will have to override this method as their center is in the middle of four cells, 
        # unlike the other minos that have their center exactly on a cell.
        # 
        # How it works:
        # - First, get the positions of the four blocks relative to its center
        # - Then, rotate it into the correct orientation followed by a translation to get the actual positions of the blocks 
        normalised_positions = self.normalised_positions
        block_positions = []
        for block in normalised_positions:
            # Rotate to correct orientation
            correctly_oriented = block
            for _ in range(ROTATIONS_REQUIRED[self.orientation]):
                correctly_oriented = rotate(correctly_oriented)

            # And then add mino's center position to each to get actual position
            actual_position = correctly_oriented + self.center
            block_positions.append(actual_position)
        
        return block_positions


@dataclass
class IMino(Mino):
    center: GridPosition = GridPosition(5, 19)
    colour: str = 'light blue'

    @property 
    def blocks(self) -> list[Position]:
        match self.orientation:
            case Orientation.UP:
                block1 = self.center.top_left_position
                block2 = self.center.top_right_position
                block3 = block1 + Position(-1, 0)
                block4 = block2 + Position(1, 0)
            case Orientation.RIGHT:
                block1 = self.center.top_right_position
                block2 = block1 + Position(0, 1)
                block3 = self.center.bottom_right_position
                block4 = block3 + Position(0, -1)
            case Orientation.DOWN:
                block1 = self.center.bottom_left_position
                block2 = self.center.bottom_right_position
                block3 = block1 + Position(-1, 0)
                block4 = block2 + Position(1, 0)
            case Orientation.LEFT:
                block1 = self.center.top_left_position
                block2 = block1 + Position(0, 1)
                block3 = self.center.bottom_left_position
                block4 = block3 + Position(0, -1)

        return [block1, block2, block3, block4]

    @property
    def normalised_positions(self):
        return [
            Position(-1,1),
            Position(0,1),
            Position(1,1),
            Position(2,1)
        ]

@dataclass
class OMino(Mino):
    center: GridPosition = GridPosition(5, 19)
    colour: str = 'light blue'

    @property 
    def blocks(self) -> list[Position]:
        return [
            self.center.top_left_position,
            self.center.top_right_position,
            self.center.bottom_left_position,
            self.center.bottom_right_position
        ] 
    
    @property
    def normalised_positions(self):
        return [
            Position(0,0),
            Position(0,1),
            Position(-1,0),
            Position(-1,1)
        ] 

@dataclass
class JMino(Mino):
    center: Position = Position(4, 19)
    colour = 'blue'

    @property
    def normalised_positions(self) -> list[Position]:
        return  [
            Position(-1,1), 
            Position(-1,0), 
            Position(0,0), 
            Position(1,0) 
            ]

@dataclass
class LMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'orange'

    @property
    def normalised_positions(self) -> list[Position]:
        return  [
            Position(-1,0), 
            Position(0,0), 
            Position(1,0),
            Position(1,1) 
            ]

@dataclass
class SMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'green'

    @property
    def normalised_positions(self) -> list[Position]:
        return  [
            Position(-1,0), 
            Position(0,0), 
            Position(0,1),
            Position(1,1) 
            ]

@dataclass
class ZMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'red'

    @property
    def normalised_positions(self) -> list[Position]:
        return  [
            Position(-1,1), 
            Position(0,1), 
            Position(0,0), 
            Position(1,0) 
            ]

@dataclass
class TMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'purple'

    @property
    def normalised_positions(self) -> list[Position]:
        return  [
            Position(-1,0), 
            Position(0,0), 
            Position(0,1), 
            Position(1,0) 
            ]



def create_mino(type: str) -> Mino:
    match type:
        case 'I':
            return IMino()
        case 'J':
            return JMino()
        case 'L':
            return LMino()
        case 'Z':
            return ZMino()
        case 'S':
            return SMino()
        case 'T':
            return TMino()
        case 'O':
            return OMino()

def rotate(point: Position) -> Position:
    """Rotate point 90 degrees about origin"""
    return Position(point.y, -point.x)

def test():
    a = create_mino('O')
    print(a)
    print(a.normalised_positions)
    print(a.blocks)
    a.orientation = Orientation.DOWN
    print(a.blocks)
    a.orientation = Orientation.UP
    print(a.blocks)
    a.orientation = Orientation.LEFT
    print(a.blocks)

if __name__ == '__main__':
    test()
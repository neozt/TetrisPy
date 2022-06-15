from abc import ABC, abstractproperty
from dataclasses import dataclass
from enum import Enum

from position import Position, GridPosition


class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def clockwise(self):
        return Orientation((self.value + 1) % len(Orientation))

    def counterclockwise(self):
        return Orientation((self.value - 1) % len(Orientation))


def rotations_required(start: Orientation, end: Orientation):
    return (end.value - start.value) % len(Orientation)


@dataclass
class Mino(ABC):
    center: Position | GridPosition
    orientation: Orientation = Orientation.UP

    @abstractproperty
    def normalised_positions(self) -> list[Position]:
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
        times_to_rotate = rotations_required(Orientation.UP, self.orientation)
        for block in normalised_positions:
            # Rotate to correct orientation
            correctly_oriented = block
            for _ in range(times_to_rotate):
                correctly_oriented = rotate(correctly_oriented)

            # And then add mino's center position to each to get actual position
            actual_position = correctly_oriented + self.center
            block_positions.append(actual_position)

        return block_positions

    def left(self) -> None:
        self.translate((-1, 0))

    def right(self) -> None:
        self.translate((1, 0))

    def down(self) -> None:
        self.translate((0, -1))

    def translate(self, offset: tuple[int, int]) -> None:
        x, y = offset
        self.center = self.center + Position(x, y)

    def rotate_cw(self) -> None:
        new_orientation = (self.orientation.value + 1) % len(Orientation)
        self.orientation = Orientation(new_orientation)

    def rotate_ccw(self) -> None:
        new_orientation = (self.orientation.value - 1) % len(Orientation)
        self.orientation = Orientation(new_orientation)


@dataclass
class IMino(Mino):
    center: GridPosition = GridPosition(5, 19)
    colour: str = 'blue'
    type: str = 'I'

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
            Position(-1, 1),
            Position(0, 1),
            Position(1, 1),
            Position(2, 1)
        ]


@dataclass
class OMino(Mino):
    center: GridPosition = GridPosition(5, 19)
    colour: str = 'yellow'
    type: str = 'O'

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
            Position(0, 0),
            Position(0, 1),
            Position(-1, 0),
            Position(-1, 1)
        ]


@dataclass
class JMino(Mino):
    center: Position = Position(4, 19)
    colour = 'dark blue'
    type: str = 'T'

    @property
    def normalised_positions(self) -> list[Position]:
        return [
            Position(-1, 1),
            Position(-1, 0),
            Position(0, 0),
            Position(1, 0)
        ]


@dataclass
class LMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'orange'
    type: str = 'L'

    @property
    def normalised_positions(self) -> list[Position]:
        return [
            Position(-1, 0),
            Position(0, 0),
            Position(1, 0),
            Position(1, 1)
        ]


@dataclass
class SMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'green'
    type: str = 'S'

    @property
    def normalised_positions(self) -> list[Position]:
        return [
            Position(-1, 0),
            Position(0, 0),
            Position(0, 1),
            Position(1, 1)
        ]


@dataclass
class ZMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'red'
    type: str = 'Z'

    @property
    def normalised_positions(self) -> list[Position]:
        return [
            Position(-1, 1),
            Position(0, 1),
            Position(0, 0),
            Position(1, 0)
        ]


@dataclass
class TMino(Mino):
    center: Position = Position(4, 19)
    colour: str = 'purple'
    type: str = 'T'

    @property
    def normalised_positions(self) -> list[Position]:
        return [
            Position(-1, 0),
            Position(0, 0),
            Position(0, 1),
            Position(1, 0)
        ]


def create_mino(type: str) -> Mino:
    match type:
        case 'I': return IMino()
        case 'J': return JMino()
        case 'L': return LMino()
        case 'Z': return ZMino()
        case 'S': return SMino()
        case 'T': return TMino()
        case 'O': return OMino()


def rotate(point: Position) -> Position:
    """Rotate point 90 degrees about origin"""
    return Position(point.y, -point.x)


def test():
    a = create_mino('I')
    print(a)
    print(a.blocks)
    a.rotate_cw()
    a.rotate_cw()
    print(a)
    print(a.blocks)


if __name__ == '__main__':
    test()

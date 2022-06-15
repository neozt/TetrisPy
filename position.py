from __future__ import annotations
from dataclasses import dataclass
from tkinter import Grid


@dataclass
class Position:
    x: int
    y: int

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.x}, {self.y})'

    def __add__(self, other: Position) -> Position:
        if not isinstance(other, Position):
            raise TypeError(
                'Position object can only be added to other Position objects')
        return type(self)(self.x + other.x, self.y + other.y)


@dataclass
class GridPosition(Position):
    @property
    def top_left_position(self) -> Position:
        return Position(self.x - 1, self.y)

    @property
    def top_right_position(self) -> Position:
        return Position(self.x, self.y)

    @property
    def bottom_left_position(self) -> Position:
        return Position(self.x - 1, self.y - 1)

    @property
    def bottom_right_position(self) -> Position:
        return Position(self.x, self.y - 1)


def test():
    a = GridPosition(0, 0)
    b = a + Position(3, 0)
    print(b)


if __name__ == '__main__':
    test()

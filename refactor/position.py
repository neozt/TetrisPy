from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.x}, {self.y})'

    def __add__(self, other: Position) -> Position:
        if type(other) is not type(self):
            raise TypeError('Position object can only be added to other Position objects')
        return Position(self.x + other.x, self.y + other.y)

@dataclass
class GridPosition:
    x: int
    y: int

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
    pass

if __name__ == '__main__':
    test()
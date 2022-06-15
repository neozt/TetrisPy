import random

import mino
from mino import Mino

PREVIEW_LENGTH = 5


class PieceQueue:
    def __init__(self) -> None:
        self.queue: list[Mino] = list()
        self.add_new_bag()

    def __repr__(self) -> str:
        return f'<PieceQueue: {self.queue}>'

    def add_new_bag(self) -> None:
        bag = ['I', 'L', 'J', 'T', 'S', 'Z', 'O']
        random.shuffle(bag)
        for piece in bag:
            self.queue.append(mino.create_mino(piece))

    def pop(self) -> Mino:
        if len(self.queue) <= PREVIEW_LENGTH:
            self.add_new_bag()
        return self.queue.pop(0)

    def peek(self, num: int = 1) -> Mino | list[Mino]:
        if num == 1:
            return self.queue[0]
        else:
            return self.queue[0:num]


def main():
    queue = PieceQueue(None)
    print(queue)
    arr = list()
    for i in range(5):
        arr.append(queue.pop())
    print(arr)
    print(queue)


if __name__ == '__main__':
    main()

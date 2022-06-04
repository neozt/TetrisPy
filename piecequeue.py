import mino
from mino import Mino
import random

PREVIEW_LENGTH = 5

class PieceQueue:
    def __init__(self, board):
        self.board = board
        self.queue = list()
        self.add_new_bag()
        
    def __repr__(self):
        return f'<PieceQueue: {self.queue}>'

    def add_new_bag(self):
        bag = ['I','L','J','T','S','Z','O']
        random.shuffle(bag)
        for piece in bag:
            self.queue.append(mino.create_mino(piece, self.board))

    def pop(self):
        if len(self.queue) <= PREVIEW_LENGTH:
            self.add_new_bag()
        return self.queue.pop(0)

    def peek(self, num):
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


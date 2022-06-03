from pygame.locals import *

MOVE_LEFT = K_LEFT
MOVE_RIGHT = K_RIGHT
ROTATE_CW = K_UP
ROTATE_CCW = K_z
ROTATE_180 = K_a
HOLD = K_c
SOFT_DROP = K_DOWN
HARD_DROP = K_SPACE

class MoveHandler:
    '''
    Used to determine movement of mino based on user input and game ticks
    '''

    def __init__(self, game, arr = 500):
        self.arr = arr
        self.game = game
        self.ticks = 0
        self.direction_being_held = False
        self.reset_direction()
        self.reset_move_count()

    def reset_direction(self):
        self.direction = 0
        
    def reset_move_count(self):
        self.move_count = {
            'left': 0,
            'right': 0,
            'down': 0,
            'harddrop': 0
        }

    def is_moving_left(self):
        return self.direction < 0

    def is_moving_right(self):
        return self.direction > 0

    def is_neutral(self):
        return self.direction == 0

    def left(self):
        self.direction_being_held = True
        if (self.is_neutral() or self.is_moving_right()):
            self.direction = -1
            self.move_count['left'] += 1 
        else:
            self.direction -= 1
            if (self.direction + 1) % self.arr == 0:
                self.move_count['left'] += 1 
    
    def right(self):
        self.direction_being_held = True
        if (self.is_neutral() or self.is_moving_left()):
            self.direction = 1
            self.move_count['right'] += 1 
        else:
            self.direction += 1
            if (self.direction - 1) % self.arr == 0:
                self.move_count['right'] += 1 

    def get_move_count(self):
        return self.move_count

    def tick(self):
        self.ticks += 1
        if not self.direction_being_held:
            self.direction = 0
        self.direction_being_held = False
        self.reset_move_count()

    def process_inputs(self, keys):
        if keys[MOVE_LEFT]:
            self.left()
        if keys[MOVE_RIGHT]:
            self.right()
        if keys[SOFT_DROP]:
            pass
        if keys[HARD_DROP]:
            pass
        if keys[HOLD]:
            pass
        if keys[ROTATE_CW]:
            pass
        if keys[ROTATE_CCW]:
            pass
        if keys[ROTATE_180]:
            pass

def test():
    movehandler = MoveHandler(None)
    for i in range(40):
        if i == 19:
            movehandler.left()
        else:
            movehandler.right()
        print(movehandler.direction)
        print(movehandler.get_move_count())
        movehandler.tick()
    movehandler.tick()
    movehandler.right()
    print(movehandler.direction)
    print(movehandler.get_move_count())
    movehandler.tick()
    movehandler.tick()
    movehandler.right()
    print(movehandler.direction)
    print(movehandler.get_move_count())

if __name__ == '__main__':
    test()




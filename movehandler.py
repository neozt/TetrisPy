from pygame.locals import *

MOVE_LEFT = K_LEFT
MOVE_RIGHT = K_RIGHT
ROTATE_CW = K_UP
ROTATE_CCW = K_z
ROTATE_180 = K_a
HOLD = K_c
SOFT_DROP = K_DOWN
HARD_DROP = K_SPACE

class MovementHandler:
    '''
    Used to determine movement of mino based on user input and game ticks
    '''

    def __init__(self, game, arr = 500):
        self.arr = arr
        self.game = game
        self.ticks = 0
        self.current_direction = None
        self.previous_direction = None
        self.direction_held_for = 0
        self.reset_move_count()

    def __repr__(self):
        return f'Current direction: {self.current_direction}\n previous direction: {self.previous_direction}\n held for: {self.direction_held_for}'
        
    def reset_move_count(self):
        self.move_count = {
            'left': 0,
            'right': 0,
            'down': 0,
            'harddrop': 0
        }

    def was_moving_left(self):
        return self.previous_direction == 'left'

    def was_moving_right(self):
        return self.previous_direction == 'right'

    def was_neutral(self):
        return self.previous_direction is None

    def set_direction(self, direction):
        self.current_direction = direction

    def left(self):
        self.set_direction('left')
        if self.was_moving_left():
            self.direction_held_for += 1
            if (self.direction_held_for - 1) % self.arr == 0:
                self.move_count['left'] += 1 
        else:
            self.direction_held_for = 1
            self.move_count['left'] += 1

    
    def right(self):
        self.set_direction('right')
        if self.was_moving_right():
            self.direction_held_for += 1
            if (self.direction_held_for - 1) % self.arr == 0:
                self.move_count['right'] += 1 
        else:
            self.direction_held_for = 1
            self.move_count['right'] += 1 


    def tick(self):
        print(self)
        self.ticks += 1
        if self.current_direction == 'neutral':
            self.direction_held_for = 0
        self.previous_direction = self.current_direction
        self.current_direction  = 'neutral'
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
    movehandler = MovementHandler(None)
    for i in range(40):
        movehandler.right()
        print(movehandler.direction)
        print(movehandler.get_move_count())
        movehandler.tick()
    # movehandler.tick()
    # movehandler.right()
    # print(movehandler.direction)
    # print(movehandler.get_move_count())
    # movehandler.tick()
    # movehandler.tick()
    # movehandler.right()
    # print(movehandler.direction)
    # print(movehandler.get_move_count())

if __name__ == '__main__':
    test()




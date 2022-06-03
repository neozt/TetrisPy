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
    ROTATE_DEBOUNCE = 30
    SOFT_DROP_MULTIPLIER = 4

    def __init__(self, game, arr = 1, das = 10, gravity = 20):
        self.game = game
        self.arr = arr
        self.das = das

        self.gravity = gravity
        self.soft_drop_gravity = gravity // self.SOFT_DROP_MULTIPLIER
        self.soft_dropping = False
        self.gravity_ticks = 0

        self.hard_drop_held = False
        self.hard_drop_pressed = False

        self.current_direction = None
        self.previous_direction = None
        self.direction_held_for = 0
        self.current_rotate = None
        self.previous_rotate = None
        self.previous_rotate_tick = 0
        self.reset_move_count()

    def __repr__(self):
        return f'Current direction: {self.current_direction}\n previous direction: {self.previous_direction}\n held for: {self.direction_held_for}'
        
    def reset_move_count(self):
        self.move_count = {
            'left': 0,
            'right': 0,
            'down': 0,
            'harddrop': 0,
            'rotatecw': 0,
            'rotateccw': 0
        }

    def was_moving_left(self):
        return self.previous_direction == 'left'

    def was_moving_right(self):
        return self.previous_direction == 'right'

    def was_neutral(self):
        return self.previous_direction is None

    def set_direction(self, direction):
        self.current_direction = direction

    def add_move(self, move):
        self.move_count[move] += 1

    def process_inputs(self, keys):
        self.handle_movement(keys)
        self.handle_rotation(keys)
        self.handle_drop(keys)
        if keys[HOLD]:
            pass

    def handle_movement(self, keys):
        if keys[MOVE_LEFT]:
            self.left()
        if keys[MOVE_RIGHT]:
            self.right()

    def left(self):
        self.set_direction('left')
        if self.was_moving_left():
            self.direction_held_for += 1
            if self.auto_shift_delay_over():
                self.add_move('left')
        else:
            self.direction_held_for = 1
            self.add_move('left')

    def right(self):
        self.set_direction('right')
        if self.was_moving_right():
            self.direction_held_for += 1
            if self.auto_shift_delay_over():
                self.add_move('right')
        else:
            self.direction_held_for = 1
            self.add_move('right')

    def auto_shift_delay_over(self):
        if self.direction_held_for == 1:
            return True
        elif self.direction_held_for <= self.das:
            return False
        else: 
            return ((self.direction_held_for - self.das - 1) % self.arr )== 0

    def handle_rotation(self, keys):
        if keys[ROTATE_CW]:
            self.rotate('cw')
        if keys[ROTATE_CCW]:
            self.rotate('ccw')
        if keys[ROTATE_180]:
            self.rotate('180')

    def rotate(self, direction):
        rotate_type = 'rotate' + direction
        self.current_rotate = direction
        if self.previous_rotate == self.current_rotate:
            self.previous_rotate_tick += 1
            if self.rotate_debounce_over():
                self.add_move(rotate_type)
                self.previous_rotate_tick = 0
        else:
            self.add_move(rotate_type)
            self.previous_rotate_tick = 0
    
    def rotate_debounce_over(self):
        return self.previous_rotate_tick > self.ROTATE_DEBOUNCE

    def handle_drop(self, keys):
        if keys[SOFT_DROP]:
            self.soft_dropping = True
        if keys[HARD_DROP]:
            self.hard_drop()

    def hard_drop(self):
        self.hard_drop_pressed = True
        if not self.hard_drop_held:
            self.add_move('harddrop')

    def handle_gravity(self):
        if self.soft_dropping:
            wait_time = self.soft_drop_gravity
        else:
            wait_time = self.gravity
        if self.gravity_ticks >= wait_time:
            self.add_move('down')
            self.gravity_ticks = 0

    def tick(self):
        self.tick_drop()
        self.tick_gravity()
        self.tick_movement()
        self.tick_rotation()

    def tick_drop(self):
        self.soft_dropping = False
        self.hard_drop_held = self.hard_drop_pressed
        self.hard_drop_pressed = False

    def tick_gravity(self):
        self.gravity_ticks += 1

    def tick_movement(self):
        if self.current_direction == None:
            self.direction_held_for = 0
        self.previous_direction = self.current_direction
        self.current_direction  = None
        self.reset_move_count()

    def tick_rotation(self):
        self.previous_rotate = self.current_rotate
        self.current_rotate = None
        if self.previous_rotate is None:
            self.previous_rotate_tick = 0


def test():
    keys = dict()
    keys[MOVE_LEFT] = True
    handler = MovementHandler(None)
    def p():
        print(handler.previous_rotate)
        print(handler.previous_rotate_tick)
    def ccw():
        handler.rotate('ccw')
        p()
    def cw():
        handler.rotate('cw')
        p()
    for i in range(10):
        cw()
    ccw()
    ccw()
    cw()
    ccw()
    for i in range(10):
        ccw()

if __name__ == '__main__':
    test()




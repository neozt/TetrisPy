class Hold:
    def __init__(self, game):
        self.game = game
        self.held_mino = None
        self.allow_hold = True

    def hold_mino(self, mino):
        if self.allow_hold:
            held_mino = self.held_mino
            mino.reset_position()
            self.held_mino = mino
            return held_mino
        else:
            raise Exception('Currently not allowed to hold')

    def enable_hold(self):
        self.allow_hold = True

    def disable_hold(self):
        self.allow_hold = False

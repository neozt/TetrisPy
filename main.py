from game import Game, GameInput
from view import View

def main():
    game = Game()
    view = View()
    game.register_observer(view)
    hard_drop = GameInput(hard_drop = True)
    left = GameInput(left = 1)
    rotate = GameInput(rotate_cw = 1)
    soft_drop = GameInput(soft_drop = True)

    game.update(soft_drop)
    game.update(soft_drop)
    game.update(soft_drop)
    game.update(soft_drop)
    game.update(hard_drop)

    

if __name__ == '__main__':
    

    main()

import pygame
from pygame.locals import *

from game import Game
from inputs import UserInput, InputProcessor
from view import View


def main():
    game = Game()
    view = View()
    game.register_observer(view)
    input_processor = InputProcessor()

    pygame.init()
    clock = pygame.time.Clock()

    view.render_game(game)

    while game.alive:
        # Handle termination
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game.alive = False
            elif event.type == QUIT:
                game.alive = False

        inputs = input_processor.process_inputs(
            UserInput(pygame.key.get_pressed())
        )
        game.update(inputs)

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()

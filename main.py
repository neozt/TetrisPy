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
    game.start()

    while game.alive:
        # Handle termination / reset
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.end()
                elif event.key == K_F4:
                    game.start()
            elif event.type == QUIT:
                game.end()

        # Get user input and process it to obtain game input
        inputs = input_processor.process_inputs(
            UserInput(pygame.key.get_pressed())
        )
        # Tick the game and update based on input
        game.update(inputs)

        # Limit framerate
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()

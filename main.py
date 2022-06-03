import time
import pygame
from pygame.locals import *

from game import *
from renderer import Renderer
import util

pygame.init()
screen = pygame.display.set_mode((Renderer.SCREEN_WIDTH, Renderer.SCREEN_HEIGHT))
screen.fill((255, 255, 255))

clock = pygame.time.Clock()

game = Game()
renderer = Renderer(game, screen)

while game.running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game.stop_game()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game.stop_game()
            # elif event.key == K_RIGHT:
            #     game.move_mino_right()
            # elif event.key == K_LEFT:
            #     game.move_mino_left()
            elif event.key == K_UP:
                game.mino.rotate_cw()
            elif event.key == K_z:
                game.mino.rotate_ccw()
            elif event.key == K_SPACE:
                game.hard_drop()

    keys = pygame.key.get_pressed()
    game.soft_dropping = True if keys[K_DOWN] else False

    game.process_inputs(keys)


    game.perform_moves()
    renderer.render_game()
    pygame.display.update()

    if game.check_death() == True:
        game.stop_game()
        # print(game.board.board)
        util.wait()

    cleared_lines = game.check_and_handle_line_clears()
    if cleared_lines:
        print(cleared_lines)
        renderer.line_clear_animation(cleared_lines)

    clock.tick(Renderer.FRAMERATE)
    game.handle_gravity()
    game.tick()

pygame.quit()


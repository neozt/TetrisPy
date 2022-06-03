import time
import pygame
from pygame.locals import *

from game import *
from renderer import Renderer
import util
from movehandler import MovementHandler

pygame.init()
screen = pygame.display.set_mode((Renderer.SCREEN_WIDTH, Renderer.SCREEN_HEIGHT))
screen.fill((255, 255, 255))

clock = pygame.time.Clock()

game = Game()
renderer = Renderer(game, screen)

i = 0

while game.running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game.stop_game()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game.stop_game()

    keys = pygame.key.get_pressed()
    game.process_inputs(keys)

    game.handle_gravity()
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
    i +=1
    # time.sleep(2)
    game.tick()

pygame.quit()


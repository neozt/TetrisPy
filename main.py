import time
import pygame
from pygame.locals import *

from game import *
from renderer import Renderer
import util
from movehandler import MovementHandler

pygame.init()
screen = pygame.display.set_mode((Renderer.SCREEN_WIDTH, Renderer.SCREEN_HEIGHT))

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

    keys = pygame.key.get_pressed()
    game.process_inputs(keys)

    game.handle_gravity()
    game.perform_moves()

    renderer.render_game()
    pygame.display.update()

    cleared_lines = game.check_and_handle_line_clears()
    if cleared_lines:
        print(cleared_lines)
        renderer.line_clear_animation(cleared_lines)
        
    if game.check_death() == True:
        game.stop_game()
        util.wait()

    clock.tick(Renderer.FRAMERATE)
    game.tick()

pygame.quit()


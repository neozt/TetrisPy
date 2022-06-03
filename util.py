import pygame
from pygame.locals import *

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    return
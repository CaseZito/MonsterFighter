"""
BrickBreaker keyboard controller code
"""

import pygame.locals

class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the hero """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.hero.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.hero.vx += 1.0

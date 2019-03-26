"""
BrickBreaker controller code
"""

import pygame.locals

class PyGameMouseController(object):
    """ A controller that uses the mouse to move the hero """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Handle the mouse event so the hero tracks the mouse position """
        if event.type == pygame.locals.MOUSEMOTION:
            self.model.hero.x = event.pos[0] - self.model.hero.width/2.0
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.shoot_arrow(event.pos[0], event.pos[1], 3)

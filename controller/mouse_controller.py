"""
BrickBreaker controller code
"""

import pygame.locals

class PyGameMouseController(object):
    """ A controller that uses the mouse to move the paddle """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Handle the mouse event so the paddle tracks the mouse position """
        if event.type == pygame.locals.MOUSEMOTION:
            self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0

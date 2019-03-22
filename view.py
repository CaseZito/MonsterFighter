"""
BrickBreaker view code
"""

import pygame


class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        for brick in self.model.bricks:
            pygame.draw.rect(self.screen,
                             pygame.Color(255, 255, 255),
                             pygame.Rect(brick.x,
                                         brick.y,
                                         brick.width,
                                         brick.height))
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.hero.x,
                                     self.model.hero.y,
                                     self.model.hero.width,
                                     self.model.hero.height))
        pygame.display.update()

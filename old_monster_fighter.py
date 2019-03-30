# -*- coding: utf-8 -*-
"""
This is Monster Fighter, a simple arcade game where a hero
shoots arrows at a mosnter. It uses the Model-View-Controller (MVC)
design pattern.

@author: Mellie Zito and Anthony
"""

import time
import pygame
from model import MonsterFighterModel
from view import PyGameWindowView
from controller.keyboard_controller import PyGameKeyboardController
from controller.mouse_controller import PyGameMouseController


def start_game(size):
    """
    Given screen 'size' as (x,y) tuple, start BrickBreaker game
    """
    pygame.init()

    model = MonsterFighterModel(size)
    print(model)
    view = PyGameWindowView(model, size)
    #controller = PyGameKeyboardController(model)
    controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()

if __name__ == '__main__':
    size = (640, 480)
    start_game(size)

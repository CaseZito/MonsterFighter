import time
import pygame
from helpers import *
from pygame.locals import *
from model import BrickBreakerModel
from view import PyGameWindowView
from controller.keyboard_controller import PyGameKeyboardController
from controller.mouse_controller import PyGameMouseController

class monster_fighter_main:
    def __init__(self, width = 640, height = 480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def MainLoop(self):
        self.LoadSprites()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.hero_sprites.draw(self.screen)
            pygame.display.flip()

    def LoadSprites(self):
        self.hero = Hero()
        self.hero_sprites = pygame.sprite.RenderPlain((self.hero))

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Pixel_Knight.png', -1)

if __name__ == "__main__":
    MainWindow = monster_fighter_main()
    MainWindow.MainLoop()

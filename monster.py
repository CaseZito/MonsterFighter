"""@authors: Mellie Z and Anthony K


This is Monster Fighter, a simple arcade game where a hero
shoots arrows at a mosnter.

The images for these sprites and background are not our own.
"""

import time
import random
import pygame
from helpers import *
from pygame.locals import *


class Arrow(pygame.sprite.Sprite):
    """ Encodes the state of the hero's arrows in the game """
    def __init__(self, name, damage, height, width, x, y, vy):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.name = name
        self.image, self.rect = load_image(name+'.png', -1)
        self.image = pygame.transform.scale(self.image, (height,width))
        self.rect.height = height
        self.rect.width = width
        self.rect.left = x
        self.rect.top =  y
        self.vy = vy

    def __str__(self):
        return self.name + " height=%f, width=%f, x=%f, y=%f, vy=%f" % (self.rect.height,
                                                                        self.rect.width,
                                                                        self.rect.left,
                                                                        self.rect.top,
                                                                        self.vy)

    def update(self):
        self.rect.top -= self.vy #moves w/ constant v upwards

class Cookie(Arrow): #damage is actually opposite for this class
    """Encodes the state of the hero's cookies in the game """

class Fireball(Arrow):
    """Encodes the state of the monster's fireballs in the game """

    def update(self):
        self.rect.top += self.vy #moves w/ constant v upwards

class Hero(pygame.sprite.Sprite):
    """ Encodes the state of the hero in the game """
    def __init__(self, name, health, height, width, x, y, vx):
        """ Initialize a hero with the specified health, height, width,
            and position (x,y) """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name+'.png', -1)
        self.image = pygame.transform.scale(self.image, (height,width))
        self.rect.height = height
        self.rect.width = width
        self.rect.left = x
        self.rect.top =  y
        self.name = name
        self.health = health
        self.vx = vx

    def lower_health(self, points):
        """ Lowers hero's health by given number of points"""
        self.health -= points

    def update(self, model):
        """ update the state of the hero """
        if self.alive() and pygame.sprite.spritecollide(self, model.fireball_group, True):
                self.lower_health(10)
                print('Ouch!')
                print("Hero Health is " + str(self.health) + " points")

    def __str__(self):
        return self.name + " health =%f, height=%f, width=%f, x=%f, y=%f" % (self.health,
                                                                     self.rect.height,
                                                                     self.rect.width,
                                                                     self.rect.left,
                                                                     self.rect.top)

class Monster(Hero): #framework for later
    """ Encodes the state of the monster in the game """

    def raise_health(self, points):
        """ Raises monster's health by given number of points """
        self.health += points

    def shoot_fireball(self, model):
        model.fireball = Fireball('Fireball', 10, 50, 50, self.rect.left, self.rect.top, 3)
        model.fireball_group.add(model.fireball)

    def update(self, model):
        """updates state of the monster """
        if self.rect.left >= 1100: #size of entry is 600 to 1100
            self.vx = -1 #monster moves with constant speed
        elif self.rect.left <= 600: #monster switches direction near edge of screen
            self.vx = 1

        self.rect.left += self.vx
        if self.alive() and random.randrange(50) == 1:
            self.shoot_fireball(model)

        #below code is for collision detection of monster and arrows
        if self.alive() and pygame.sprite.spritecollide(self, model.arrow_group, True):
                self.lower_health(10)
                print('ARGGG')
                print("Monster Health is " + str(self.health) + " points")


class monster_fighter_main:
    def __init__(self, width, height):
        """ Encodes the state of the game """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hero = Hero('Hero', 100, 320, 320, 0, 630, 0) #name, health, height, width, x, y, vx
        self.monster = Monster("Monster", 50, 200, 200, 947, 220, 1)
        self.arrow_group = pygame.sprite.Group()
        self.fireball_group = pygame.sprite.Group()
        #cookie_group = pygame.sprite.Group()

    def shoot_arrow(self, x, y, vy):
        """ Creates an arrow that is 'shot' by the hero """
        self.arrow = Arrow('Arrow', 10, 30, 50, x, y, vy)
        self.arrow_group.add(self.arrow)

    def update(self):
        """ Update the game state """
        self.hero.update(self) #needs model to detect fireball hit
        self.monster.update(self) #needs model for arrow hits and shooting fireballs
        self.arrow_group.update()
        self.fireball_group.update()

    def loadsprites(self):
        """ Loads sprites """
        self.hero_sprites = pygame.sprite.RenderPlain((self.hero))
        self.monster_sprites = pygame.sprite.RenderPlain((self.monster))

    def updatesprites(self):
        """ Draws updated and newly generated sprites """
        self.hero_sprites.draw(self.screen)
        self.monster_sprites.draw(self.screen)
        for arrow in self.arrow_group.sprites():
            self.arrow_sprites = pygame.sprite.RenderPlain((arrow))
            self.arrow_sprites.draw(self.screen)
        for fireball in self.fireball_group.sprites():
            self.fireball_sprites = pygame.sprite.RenderPlain((fireball))
            self.fireball_sprites.draw(self.screen)

    def __str__(self):
        """ Prints sprites, used for debugging """
        output_lines = []
        output_lines.append(str(self.hero))
        output_lines.append(str(self.monster))
        for arrow in self.arrow_group.sprites():
            output_lines.append(str(arrow))
        for fireball in self.fireball_group.sprites():
            output_lines.append(str(fireball))
        # print one item per line
        return "\n".join(output_lines)

    def MainLoop(self):
        """ Runs the game which includes the controller, image loading, and updating """
        print(self)
        dungeon_image, dungeon_rect = load_image('Dungeon.png', -1)
        self.loadsprites()
        while 1:
            if self.monster.alive() and self.monster.health <= 0: #when monster dies
                self.monster.kill()
                print("You have killed the monster!")
                time.sleep(.001)
                sys.exit() #without this game can continue to run without monster 
            if self.hero.health <= 0: #when hero dies
                self.hero.kill()
                print("GAME OVER")
                time.sleep(.001)
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.locals.MOUSEMOTION:
                    self.hero.rect.left = event.pos[0] - self.hero.rect.width/2.0
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.shoot_arrow(event.pos[0], self.hero.rect.top, 3)
            self.screen.blit(dungeon_image, (0,0))
            time.sleep(.001)
            self.update()
            self.updatesprites()
            pygame.display.flip()


if __name__ == "__main__":
    size = (1874, 958)
    MainWindow = monster_fighter_main(size[0], size[1])
    MainWindow.MainLoop()

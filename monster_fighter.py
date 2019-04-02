"""@authors: Mellie Z and Anthony K

This is Monster Fighter, a simple arcade game. You are the hero.
Left click to shoot arrows, right click to shoot cookies. Avoid the
monster fireballs!

The images for these sprites and background are not our own.

Hero link: https://www.pixilart.com/art/pixel-knight-49ba01ba95b0235
(Couldn't find original source^)
Monster link: https://forum.dungeonboss.com/discussion/3253/dungeon-boss-hero-pixel-art
Arrow link: unknown
Cookie link: http://pixelartmaker.com/art/794909cfeff2fe7
Fireball link: https://minecraft.novaskin.me/skin/1265863046/fireball-png
"""

import os, sys
import time
import random
import pygame
from pygame.locals import *

def load_image(name):
    """ Loads images and makes rectangles for sprites """
    image = pygame.image.load(name)
    image = image.convert()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Arrow(pygame.sprite.Sprite):
    """ Encodes the state of the hero's arrows in the game """
    def __init__(self, name, damage, height, width, x, y, vy):
        """ Initialize an Arrow with the specified damage, name, height, width,
            and position (x,y) """
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.name = name
        self.image, self.rect = load_image(name+'.png')
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
        """ Updates the state of the Arrow """
        self.rect.top -= self.vy #moves w/ constant v upwards

class Cookie(Arrow): #damage is actually opposite for this class
    """Encodes the state of the hero's cookies in the game """

class Fireball(Arrow):
    """Encodes the state of the monster's Fireballs in the game """

    def update(self):
        """ Updates the state of the Fireball """
        self.rect.top += self.vy #moves w/ constant v upwards

class Hero(pygame.sprite.Sprite):
    """ Encodes the state of the hero in the game """
    def __init__(self, name, health, height, width, x, y, vx):
        """ Initialize a hero with the specified health, height, width,
            and position (x,y) """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name+'.png')
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
        """ Updates the state of the hero """
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
        """ Creates fireball, which monster then 'shoots'"""
        centerx = self.rect.left + (self.rect.width/4) #to shoot fireball from center of monster
        centery =  self.rect.top + 60
        model.fireball = Fireball('Fireball', 10, 50, 50, centerx, centery, 3)
        model.fireball_group.add(model.fireball)

    def update(self, model):
        """updates state of the monster """
        if self.rect.left >= 1100: #monster switches direction near edge of screen
            self.vx = -2 #monster moves with constant speed
        elif self.rect.left <= 600: #size of end of tunnel is 600 to 1100
            self.vx = 2

        self.rect.left += self.vx
        if self.alive() and random.randrange(50) == 1:
            self.shoot_fireball(model)

        #below code is for collision detection of monster and arrows
        if self.alive() and pygame.sprite.spritecollide(self, model.arrow_group, True):
                self.lower_health(10)
                print('ARGGG')
                print("Monster Health is " + str(self.health) + " points")

        #below code is for collision detection of monster and cookie
        if self.alive() and pygame.sprite.spritecollide(self, model.cookie_group, True):
                self.raise_health(10)
                print('Oh? Thanks..')
                print("Monster Health is " + str(self.health) + " points")


class Monster_Fighter_Main:
    """ Encodes the state of the game """
    def __init__(self, width, height):
        """ Initialize the game with the screen size and sprites """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hero = Hero('Hero', 250, 320, 320, 0, 630, 0) #name, health, height, width, x, y, vx
        self.monster = Monster("Monster", 150, 200, 200, 947, 220, 2)
        self.arrow_group = pygame.sprite.Group()
        self.fireball_group = pygame.sprite.Group()
        self.cookie_group = pygame.sprite.Group()

    def shoot_arrow(self, x, y, vy):
        """ Creates an arrow that is 'shot' by the hero """
        self.arrow = Arrow('Arrow', 10, 30, 50, x, y, vy)
        self.arrow_group.add(self.arrow)

    def shoot_cookie(self, x, y, vy):
        """ Creates a cookie that is 'shot' by the hero """
        self.cookie = Cookie('Cookie', 10, 50, 50, x, y, vy)
        self.cookie_group.add(self.cookie)

    def update(self):
        """ Update the game state """
        self.hero.update(self) #needs model to detect fireball hit
        self.monster.update(self) #needs model for arrow hits and shooting fireballs
        self.arrow_group.update()
        self.fireball_group.update()
        self.cookie_group.update()

    def load_sprites(self):
        """ Loads sprites """
        self.hero_sprites = pygame.sprite.RenderPlain((self.hero))
        self.monster_sprites = pygame.sprite.RenderPlain((self.monster))

    def update_sprites(self):
        """ Draws updated and newly generated sprites """
        self.hero_sprites.draw(self.screen)
        self.monster_sprites.draw(self.screen)
        for arrow in self.arrow_group.sprites():
            self.arrow_sprites = pygame.sprite.RenderPlain((arrow))
            self.arrow_sprites.draw(self.screen)
        for fireball in self.fireball_group.sprites():
            self.fireball_sprites = pygame.sprite.RenderPlain((fireball))
            self.fireball_sprites.draw(self.screen)
        for cookie in self.cookie_group.sprites():
            self.cookie_sprites = pygame.sprite.RenderPlain((cookie))
            self.cookie_sprites.draw(self.screen)

    def check_end_event(self):
        """ Checks if any of end events of game occur """
        if self.monster.alive() and self.monster.health <= 0: #monster dies
            self.monster.kill()
            text = "You have killed the monster!"
            exit = True #without this game can continue to run without monster
        elif self.monster.alive() and self.monster.health >= 300: #monster friended
            self.monster.rect.top -= 20 #monster walks off screen
            self.monster.kill()
            text = "The monster is your friend and appears to have walked away"
            exit = True #without this game can continue to run without monster
        elif self.hero.health <= 0: #hero dies
            self.hero.kill()
            text = "GAME OVER"
            exit = True
        else:
            text = ""
            exit = False
        return (text, exit)

    def __str__(self):
        """ Prints sprites, used for debugging """
        output_lines = []
        output_lines.append(str(self.hero))
        output_lines.append(str(self.monster))
        for arrow in self.arrow_group.sprites():
            output_lines.append(str(arrow))
        for fireball in self.fireball_group.sprites():
            output_lines.append(str(fireball))
        for cookie in self.cookie_group.sprites():
            output_lines.append(str(cookie))
        # print one item per line
        return "\n".join(output_lines)

    def MainLoop(self):
        """ Runs the game which includes the controller, image loading, and updating """
        print(self)
        dungeon_image, dungeon_rect = load_image('Dungeon.png')
        self.load_sprites()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.locals.MOUSEMOTION:
                    self.hero.rect.left = event.pos[0] - self.hero.rect.width/2.0
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.shoot_arrow(event.pos[0], self.hero.rect.top, 3)
                        if event.button == 3:
                            self.shoot_cookie(event.pos[0], self.hero.rect.top, 3)
            self.screen.blit(dungeon_image, (0,0))
            time.sleep(.001)

            text, exit = self.check_end_event() #checks if ending event occurs
            if text != "": #prints ending text if ending event occurs
                print(text)

            self.update() #updates state of game
            self.update_sprites()
            pygame.display.flip()

            if exit == True: #exits game if ending event occurs
                time.sleep(1)
                sys.exit()


if __name__ == "__main__":
    size = (1874, 958)
    MainWindow = Monster_Fighter_Main(size[0], size[1])
    MainWindow.MainLoop()

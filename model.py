"""
BrickBreaker model code
"""
import pygame

class Brick(pygame.sprite.Sprite): #changed object to sprite for collision
    """ Encodes the state of a brick in the game """
    def __init__(self,height,width,x,y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return "Brick height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)

class Hero(pygame.sprite.Sprite):
    """ Encodes the state of the hero in the game """
    def __init__(self, height, width, x, y):
        """ Initialize a hero with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0

    def update(self):
        """ update the state of the hero """
        #add a constraint for position to stop at wall
        self.x += self.vx

        #sprite.spritecollide(Hero, Arrow) this will be used for collision detection


    def __str__(self):
        return "Hero height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)

class BrickBreakerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.bricks = []
        self.width = size[0] #screen parameters
        self.height = size[1]
        self.brick_width = 100
        self.brick_height = 20
        self.brick_space = 10
        for x in range(self.brick_space,
                       self.width - self.brick_space - self.brick_width,
                       self.brick_width + self.brick_space):
            for y in range(self.brick_space,
                           self.height//2,
                           self.brick_height + self.brick_space):
                self.bricks.append(Brick(self.brick_height,
                                         self.brick_width,
                                         x,
                                         y))
        self.hero = Hero(20, 100, 200, self.height - 30)

    def update(self):
        """ Update the game state (currently only tracking the hero) """
        self.hero.update()
        
        #hero_health = pygame.sprite.Group()
        #hero_health.add(hero) #adds hero to group
        #hero_health.add(brick) #will be fireball not brick

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for brick in self.bricks:
            output_lines.append(str(brick))
        output_lines.append(str(self.hero))
        # print one item per line
        return "\n".join(output_lines)

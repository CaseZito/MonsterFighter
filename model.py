"""
MonsterFighter model code
"""

import pygame

class Arrow(pygame.sprite.Sprite):
    """ Encodes the state of the hero's arrows in the game """
    def __init__(self, damage, height, width,x,y,vy):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.damage = damage
        self.rect.height = height
        self.rect.width = width
        self.rect.left = x
        self.rect.top = y
        self.vy = vy

    def __str__(self):
        return "Arrow height=%f, width=%f, x=%f, y=%f" % (self.rect.height,
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
    def __init__(self, name, health, x, y, vx):
        """ Initialize a hero with the specified health, height, width,
            and position (x,y) """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Pixel_Knight.png', -1)
        self.image = pygame.transform.scale(self.image, (200,200))

        #self.rect.left = x
        #self.rect.top =  y
        self.name = name
        self.health = health
        self.vx = vx

    def lower_health(self, points):
        """ Lowers hero's health by given number of points"""
        self.health -= points

    def update(self):
        """ update the state of the hero """
        self.rect.left += self.vx

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
        model.fireball = Fireball(10, 30, 10, self.rect.left, self.rect.top, 3)
        model.fireball_group.add(model.fireball)

    def update(self, model, proj_group):
        """updates state of the monster """
        if self.rect.left >= 620: #size of screen is 0-640
            self.vx = -0.5 #monster moves with constant speed
        elif self.rect.left < 30: #monster switches direction near edge of screen
            self.vx = 0.5

        self.rect.left += self.vx
        self.shoot_fireball(model)

        for a in model.arrow_group.sprites():
            if self.rect.top == a.rect.top and -100 < self.rect.left - a.rect.left < 0:
                print("ARGGG")
                self.lower_health(10)
                print(self)
                a.kill()
        #hero_hit = pygame.sprite.spritecollide(self, proj_group, True)
        #if hero_hit:
                #self.lower_health(10)
                #print(self)

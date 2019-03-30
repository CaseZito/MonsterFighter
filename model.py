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
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = vy
        self.rect = pygame.Rect((x,y),(width,height))

    def __str__(self):
        return "Arrow height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y,
                                                          self.vy)

    def update(self):
        self.y -= self.vy #moves w/ constant v upwards

class Cookie(Arrow): #damage is actually opposite for this class
    """Encodes the state of the hero's cookies in the game """

class Fireball(Arrow):
    """Encodes the state of the monster's fireballs in the game """

    def update(self):
        self.y += self.vy #moves w/ constant v upwards

class Hero(pygame.sprite.Sprite):
    """ Encodes the state of the hero in the game """
    def __init__(self, name, health, height, width, x, y, vx):
        """ Initialize a hero with the specified health, height, width,
            and position (x,y) """
        #can be used once we have pixel art for character
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image(name+'.png',-1)
        #self.image, self.rect = pygame.image.load('Pixel_Knight.png')

        self.name = name
        self.health = health
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = vx
        self.rect = pygame.Rect((x,y),(width,height))

    def lower_health(self, points):
        """ Lowers hero's health by given number of points"""
        self.health -= points
        #to be used when fireball hits hero

    def update(self):
        """ update the state of the hero """
        #add a constraint for position to stop at wall
        self.x += self.vx
        #health should only decrease

        #this will be used for collision detection:
        #monster_hit = sprite.spritecollide(hero, fireball_group, True)
        #if monster_hit:
        #   #change health attribute of hero

    def __str__(self): #unsure how to change "hero" to "monster" in monster class
        return self.name + " health =%f, height=%f, width=%f, x=%f, y=%f" % (self.health,
                                                                     self.height,
                                                                     self.width,
                                                                     self.x,
                                                                     self.y)

class Monster(Hero): #framework for later
    """ Encodes the state of the monster in the game """

    def raise_health(self, points):
        """ Raises monster's health by given number of points """
        self.health += points

    def shoot_fireball(self, model):
        model.fireball = Fireball(10, 30, 10, self.x, self.y, 3)
        model.fireball_group.add(model.fireball)

    def update(self, model, proj_group):
        """updates state of the monster """
        if self.x >= 620: #size of screen is 0-640
            self.vx = -0.5 #monster moves with constant speed
        elif self.x < 30: #monster switches direction near edge of screen
            self.vx = 0.5

        self.x += self.vx
        self.shoot_fireball(model)

        for a in model.arrow_group.sprites():
            if self.y == a.y and -100 < self.x - a.x < 0:
                print("ARGGG")
                self.lower_health(10)
                print(self)
                
        #hero_hit = pygame.sprite.spritecollide(self, proj_group, True)
        #if hero_hit:
                #self.lower_health(10)
                #print(self)

class MonsterFighterModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]

        self.hero = Hero("Hero", 100, 20, 100, 200, self.height - 30, 0)
        self.monster = Monster("Monster", 50, 20, 100, 200, 0, 0.5)
        self.arrow_group = pygame.sprite.Group()
        self.fireball_group = pygame.sprite.Group()
        #cookie_group = pygame.sprite.Group()

    def shoot_arrow(self, x, y, vy):
        self.arrow = Arrow(10, 30, 10, x, y, vy)
        self.arrow_group.add(self.arrow)

    def update(self):
        """ Update the game state (currently only tracking the hero) """
        self.hero.update()
        self.monster.update(self, self.arrow_group)
        self.arrow_group.update()
        self.fireball_group.update()

    def __str__(self):
        output_lines = []
        output_lines.append(str(self.hero))
        output_lines.append(str(self.monster))
        # print one item per line
        return "\n".join(output_lines)

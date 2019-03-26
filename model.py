"""
BrickBreaker model code
"""
import pygame

class Brick(pygame.sprite.Sprite): #going to be health bar
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

class Arrow(pygame.sprite.Sprite):
    """ Encodes the state of the hero's arrows in the game """
    def __init__(self, damage, height, width,x,y,vy):
        self.damage = damage
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = vy

    def __str__(self):
        return "Arrow height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y,
                                                          self.vy)

    def update(self):
        self.y += self.vy #moves w/ constant v upwards

class Cookie(Arrow): #damage is actually opposite for this class
    """Encodes the state of the hero's cookies in the game """

class Fireball(Arrow):
    """Encodes the state of the monster's fireballs in the game """

class Hero(pygame.sprite.Sprite):
    """ Encodes the state of the hero in the game """
    def __init__(self, name, health, height, width, x, y, vx):
        """ Initialize a hero with the specified health, height, width,
            and position (x,y) """
        #can be used once we have pixel art for character
        #pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image(name+'.png',-1)
        self.name = name
        self.health = health
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = vx

    def lower_heatlh(self, points):
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

    def update(self):
        """updates state of the monster """
        if self.x >= 620: #size of screen is 0-640
            self.vx = -0.5 #monster moves with constant speed
        elif self.x < 30: #monster switches direction near edge of screen
            self.vx = 0.5

        self.x += self.vx
        #health can increase and decrease depending on arrow or cookie

        #this will be used for collision detection:
        #hero_hit = sprite.spritecollide(monster, arrow_group, True)
        #if hero_hit:
        #   #change health attribute

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
        self.hero = Hero("Hero", 100, 20, 100, 200, self.height - 30, 0)
        self.monster = Monster("Monster", 50, 20, 100, 200, self.height - 50, 0.5)

        self.arrow_group = pygame.sprite.Group()
        #arrow_group.add(arrow)

        #cookie_group = pygame.sprite.Group()
        #cookie_group.add(cookie)

        #fireball_group = pygame.sprite.Group()
        #fireball_group.add(fireball)
    def shoot_arrow(self, x, y, vy):
        self.arrow = Arrow(10, 3, 1, x, y, vy)
        self.arrow_group.add(self.arrow)

    def update(self):
        """ Update the game state (currently only tracking the hero) """
        self.hero.update()
        self.monster.update()
        self.arrow_group.update()

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for brick in self.bricks:
            output_lines.append(str(brick))
        output_lines.append(str(self.hero))
        output_lines.append(str(self.monster))
        # print one item per line
        return "\n".join(output_lines)

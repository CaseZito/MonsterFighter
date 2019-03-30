"""
@author: Mellie Zito and Anthony K
"""

import pygame
import pygame.locals
import time

class Arrow(pygame.sprite.Sprite):
    """ Encodes the state of the hero's arrows in the game """
    def __init__(self, damage, height, width,x,y,vy):
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

    def update(self, proj_group):
        """updates state of the monster """
        if self.x >= 620: #size of screen is 0-640
            self.vx = -0.5 #monster moves with constant speed
        elif self.x < 30: #monster switches direction near edge of screen
            self.vx = 0.5

        self.x += self.vx
        #health can increase and decrease depending on arrow or cookie
        #this will be used for collision detection:

        hero_hit = pygame.sprite.spritecollide(self, proj_group, True)
        if hero_hit:
            print("HEY")
            self.lower_health(10)
            print(self)

class MonsterFighterModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]

        self.hero = Hero("Hero", 100, 20, 100, 200, self.height - 30, 0)
        self.monster = Monster("Monster", 50, 20, 100, 200, 0, 0.5)
        self.hero_sprites = pygame.sprite.RenderPlain((self.hero))
        self.arrow_group = pygame.sprite.Group()
        #arrow_group.add(arrow)

        #cookie_group = pygame.sprite.Group()
        #cookie_group.add(cookie)

        #fireball_group = pygame.sprite.Group()
        #fireball_group.add(fireball)
    def shoot_arrow(self, x, y, vy):
        self.arrow = Arrow(10, 30, 10, x, y, vy)
        self.arrow_group.add(self.arrow)

    def update(self):
        """ Update the game state (currently only tracking the hero) """
        self.hero.update()
        self.arrow_group.update()
        self.monster.update(self.arrow_group)

    def __str__(self):
        output_lines = []
        output_lines.append(str(self.hero))
        output_lines.append(str(self.monster))
        # print one item per line
        return "\n".join(output_lines)



"""
MonsterFighter view code
"""


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

        #self.hero_sprites.draw(self.screen)

        pygame.draw.rect(self.screen,
                         pygame.Color(0, 0, 255),
                         pygame.Rect(self.model.hero.x,
                                     self.model.hero.y,
                                     self.model.hero.width,
                                     self.model.hero.height))

        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.monster.x,
                                     self.model.monster.y,
                                     self.model.monster.width,
                                     self.model.monster.height))

        for arrow in self.model.arrow_group.sprites():
            pygame.draw.rect(self.screen,
                             pygame.Color(0, 255, 0),
                             pygame.Rect(self.model.arrow.x,
                                         self.model.arrow.y,
                                         self.model.arrow.width,
                                         self.model.arrow.height))
        pygame.display.update()




"""
BrickBreaker controller code
"""

class PyGameMouseController(object):
    """ A controller that uses the mouse to move the hero """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Handle the mouse event so the hero tracks the mouse position """
        if event.type == pygame.locals.MOUSEMOTION:
            self.model.hero.x = event.pos[0] - self.model.hero.width/2.0
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.shoot_arrow(event.pos[0], self.model.hero.y, 3)




"""
Monster final code
"""

def start_game(size):
    """
    Given screen 'size' as (x,y) tuple, start BrickBreaker game
    """
    pygame.init()

    model = MonsterFighterModel(size)
    print(model)
    view = PyGameWindowView(model, size)
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

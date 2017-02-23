import pygame as pg
from os import path
import math, random, spritesheet

balloon_width = 48
balloon_height = 68
balloon_image = None

def get_balloon_image():
    global balloon_image, balloon_width, balloon_height
    if balloon_image == None:
        ss = spritesheet.spritesheet(path.join('images','RedBalloonSprites.png'))    
        top_offset = 6
        left_offset = 12

        x = left_offset
        y = top_offset
        balloon_image = ss.image_at((x,y, balloon_width, balloon_height), colorkey=(84,110,140))

    return balloon_image
    
    
class MovingItem(object):

    def __init__(self, screen, (x, y), image, angle, velocity, gravity):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image
        self.size = self.image.get_rect().size
        self.velocity = velocity
        #convert angle to radias
        self.angle = angle / 180.0 * math.pi
        self.xVelocity = math.cos(self.angle) * velocity
        self.yVelocity = math.sin(self.angle) * velocity
        self.gravity = gravity
        self.time = 0.0

    def update(self, wind):
        self.time += .05

        self.x += (self.xVelocity * self.time) + (.5 * (wind / 5.0) * self.time ** 2)
        self.y += ((-1.0 * (self.yVelocity * self.time)) + (.5 * self.gravity * (self.time ** 2))) 

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Balloon(MovingItem):

    def __init__(self, screen, xLow, xHigh, yLow, yHigh):
        velocity = random.randrange(30,60,1) / 1000.0
        x = random.randint(xLow,xHigh)
        y = random.randint(yLow, yHigh)
        image = get_balloon_image()
        angle = 90
        gravity = 0.0005
        super(Balloon, self).__init__(screen, (x,y),image, angle, velocity, gravity)

    def is_offscreen(self):
        if self.y + balloon_height < 0:
            return True
        return False

    def is_hit(self, x, y):
        rect = pg.Rect( (self.x, self.y), self.size )
        hit = rect.collidepoint(x,y)
        if hit:
            print "balloon popped %s %s at point %s %s" % (self.x,self.y, x,y)

        return hit


class Rock(MovingItem):
    
    def __init__(self, screen, (x,y), angle, velocity):
        image = pg.image.load(path.join('images','stone.png'))
        gravity_of_earth = 9.8
        super(Rock, self).__init__(screen, (x,y),image, angle, velocity, gravity_of_earth)
        self.time = 0.2
    def hit_balloon(self,balloons):
        for balloon in balloons:
            if balloon.is_hit(self.x,self.y):
                return balloon
        return None

 
import pygame as pg
from os import path

class Person(object):
    """The slingshot boy class.
    """

    def __init__(self, screen, (x, y), angle):
        """ Constructor is called when the class has been instantiated
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
        # four images are used for walking
        self.moving_images = [pg.image.load(path.join('images','walk1.png')),
            pg.image.load(path.join('images','walk2.png')),
            pg.image.load(path.join('images','walk3.png')),
            pg.image.load(path.join('images','walk4.png'))]
        self.image = self.moving_images[0]
        self.image_number = 0

        # One image for aiming the slingshot
        self.aim_image = pg.image.load(path.join('images','stayattack1.png'))

        # Three images for firing the slingshot
        self.fire_images = [pg.image.load(path.join('images','stayattack2.png')),
            pg.image.load(path.join('images','stayattack3.png')),
            pg.image.load(path.join('images','stayattack4.png'))]
        self.fire_image_number = 0

    def draw(self):
        ### Add the current image to display to the screen
        self.screen.blit(self.image, (self.x, self.y))

    def move_left(self, step):
        # Move the person left, along the x axis, don't let him off the screen
        self.x -= step
        if self.x < 0:
            self.x = 0

        self.image_number -= 1
        if self.image_number < 0:
            self.image_number = 3
        self.image = self.moving_images[self.image_number]
    
    def move_right(self, step):
        # Move the person right, along the x axis
        # Invisible barrier to make it more difficult
        self.x += step
        if self.x > 500:
            self.x = 500
            
        self.image_number += 1
        if self.image_number > 3:
            self.image_number = 0
        self.image = self.moving_images[self.image_number]

    def increase_angle(self, step):
        # Increase the angle used to throw the rock, stopping at straight up
        self.angle += step
        if self.angle > 90:
            self.angle = 90

    def decrease_angle(self, step):
        # Decrease the angle used to throw the rock, stopping at straight across
        self.angle -= step
        if self.angle < 0:
            self.angle = 0

    def aim(self):
        # Assign the aim image
        self.image = self.aim_image
        self.image_number = 0
        self.fire_image_number = 0

    def fire(self):
        # assign the fire image, increasing the fire image counter
        # return true when the last image has been loaded
        if self.fire_image_number > 2:
            self.fire_image_number = 2
        self.image = self.fire_images[self.fire_image_number]
        self.fire_image_number += 1
        return self.fire_image_number > 2
        

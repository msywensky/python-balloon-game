import pygame as pg
from os import path

class Person(object):

    def __init__(self, screen, (x, y), angle):
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
    
        self.moving_images = [pg.image.load(path.join('images','walk1.png')),
            pg.image.load(path.join('images','walk2.png')),
            pg.image.load(path.join('images','walk3.png')),
            pg.image.load(path.join('images','walk4.png'))]
        self.image = self.moving_images[0]
        self.image_number = 0
        self.aim_image = pg.image.load(path.join('images','stayattack1.png'))
        self.fire_images = [pg.image.load(path.join('images','stayattack2.png')),
            pg.image.load(path.join('images','stayattack3.png')),
            pg.image.load(path.join('images','stayattack4.png'))]
        self.fire_image_number = 0

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move_left(self, step):
        self.x -= step
        if self.x < 0:
            self.x = 0

        self.image_number -= 1
        if self.image_number < 0:
            self.image_number = 3
        self.image = self.moving_images[self.image_number]
    
    def move_right(self, step):
        self.x += step
        if self.x > 500:
            self.x = 500
            
        self.image_number += 1
        if self.image_number > 3:
            self.image_number = 0
        self.image = self.moving_images[self.image_number]

    def increase_angle(self, step):
        self.angle += step
        if self.angle > 90:
            self.angle = 90

    def decrease_angle(self, step):
        self.angle -= step
        if self.angle < 0:
            self.angle = 0

    def aim(self):
        self.image = self.aim_image
        self.image_number = 0
        self.fire_image_number = 0

    def fire(self):
        if self.fire_image_number > 2:
            self.fire_image_number = 2
        self.image = self.fire_images[self.fire_image_number]
        self.fire_image_number += 1
        return self.fire_image_number > 2
        

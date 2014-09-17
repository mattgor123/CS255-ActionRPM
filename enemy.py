import pygame as game
import random

class enemy(game.sprite.Sprite):
    #These are the images, images are default
    image = None
    right = None
    left = None
    up = None
    down = None
    xspeed = 0
    yspeed = 0
    direction = "right"

    def __init__(self, location):
        game.sprite.Sprite.__init__(self)

        if enemy.image is None:
            enemy.image = game.image.load("images/enemyfullhealth.png")
            enemy.right = enemy.image
            enemy.left  = game.transform.rotate(enemy.right, 180)
            enemy.up  = game.transform.rotate(enemy.right, 90)
            enemy.down  = game.transform.rotate(enemy.right, -90)

        self.image = enemy.image
        self.xspeed = random.randint(1,5)
        self.yspeed = random.randint(1,5)
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self):
        self.rect = self.rect.move(self.xspeed,self.yspeed)
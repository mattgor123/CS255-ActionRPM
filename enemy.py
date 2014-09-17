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

    def __init__(self, location, speed, direction):
        game.sprite.Sprite.__init__(self)
        print(direction)
        if enemy.image is None:
            enemy.image = game.image.load("images/enemyfullhealth.png")
            enemy.right = enemy.image
            enemy.left  = game.transform.rotate(enemy.right, 180)
            enemy.up  = game.transform.rotate(enemy.right, 90)
            enemy.down  = game.transform.rotate(enemy.right, -90)
            enemy.upright  = game.transform.rotate(enemy.right, 45)
            enemy.upleft  = game.transform.rotate(enemy.right, 135)
            enemy.downright  = game.transform.rotate(enemy.right, -45)
            enemy.downleft  = game.transform.rotate(enemy.right, -135)

        if (direction == 1):
            self.direction="right"
            self.image = enemy.right
            print("setting right")
        elif (direction == 2):
            self.direction="downright"
            self.image = enemy.downright
            print("setting downright")
        elif (direction == 3):
            self.direction="down"
            self.image = enemy.down
        elif (direction == 4):
            self.direction="downleft"
            self.image = enemy.downleft
        elif (direction == 5):
            self.direction="left"
            self.image = enemy.left
        elif (direction == 6):
            self.direction="upleft"
            self.image = enemy.upleft
        elif (direction == 7):
            self.direction="up"
            self.image = enemy.up
        elif (direction == 8):
            self.direction="upright"
            self.image = enemy.upright

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self):
        if self.direction == "upleft":
            #COLLISIONDETECT & UPDATE DIRECTION NEEDS TO BE ADDED
            self.rect =  self.rect.move(-self.speed,-self.speed)

        elif self.direction == "downleft":
            self.rect =  self.rect.move(-self.speed,+self.speed)

        elif self.direction == "upright":
            self.rect =  self.rect.move(self.speed,-self.speed)

        elif self.direction == "downright":
            self.rect =  self.rect.move(self.speed,self.speed)

        elif self.direction == "right":
            self.rect =  self.rect.move(self.speed,0)

        elif self.direction == "up":
            self.rect =  self.rect.move(0,-self.speed)

        elif self.direction == "down":
            self.rect =  self.rect.move(0,self.speed)

        elif self.direction == "left":
            self.rect =  self.rect.move(-self.speed,0)

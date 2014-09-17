import pygame as game
import random

class enemy(game.sprite.Sprite):
    image = None
    screenwidth = 0
    screenheight = 0

    #enemy constructor takes an initial location, screendims for collisions, a speed, and a starting direction
    def __init__(self, location, screensize, speed, direction):
        game.sprite.Sprite.__init__(self)
        enemy.screenwidth = screensize[0]
        enemy.screenheight = screensize[1]
        if enemy.image is None:
            #make all of the appropriate transformations of the image based on direction of travel
            enemy.image = game.image.load("images/enemyfullhealth.png")
            enemy.right = enemy.image
            enemy.left  = game.transform.rotate(enemy.right, 180)
            enemy.up  = game.transform.rotate(enemy.right, 90)
            enemy.down  = game.transform.rotate(enemy.right, -90)
            enemy.upright  = game.transform.rotate(enemy.right, 45)
            enemy.upleft  = game.transform.rotate(enemy.right, 135)
            enemy.downright  = game.transform.rotate(enemy.right, -45)
            enemy.downleft  = game.transform.rotate(enemy.right, -135)

        #set the image based on the direction
        if (direction == 1):
            self.setdirection("right")
        elif (direction == 2):
            self.setdirection("downright")
        elif (direction == 3):
            self.setdirection("down")
        elif (direction == 4):
            self.setdirection("downleft")
        elif (direction == 5):
            self.setdirection("left")
        elif (direction == 6):
            self.setdirection("upleft")
        elif (direction == 7):
            self.setdirection("up")
        elif (direction == 8):
            self.setdirection("upright")

        #set the speed & get the rectangle
        self.speed = speed
        self.rect = self.image.get_rect()
        #make sure it is in the appropriate location
        self.rect.topleft = location
        #get the width & height of screen
        self.width = screensize[0]
        self.height = screensize[1]

    #this is the update method with a parameter - it ensures the enemy is facing opposite dir of the player then updates
    def update(self,dirchanged, direction, interval):
        if dirchanged == True:
            if direction == "right" and self.direction != "left":
                self.setdirection("left")
            elif direction == "downright" and self.direction != "upleft":
                self.setdirection("upleft")
            elif direction == "down" and self.direction != "up":
                self.setdirection("up")
            elif direction == "downleft" and self.direction != "upright":
                self.setdirection("upright")
            elif direction == "left" and self.direction != "right":
                self.setdirection("right")
            elif direction == "upleft" and self.direction != "downright":
                self.setdirection("downright")
            elif direction == "up" and self.direction != "down":
                self.setdirection("down")
            elif direction == "upright" and self.direction != "downleft":
                self.setdirection("downleft")
        self.move(interval)

    #this moves the enemy to where he is supposed to be based on the direction
    def move(self, interval):
        if self.direction == "upleft":
            self.rect =  self.rect.move(-self.speed*interval,-self.speed*interval)
            #Two possible collisions are top & left (or corner)
            if self.rect.top < 0 and self.rect.left < 0:
                self.setdirection("downright")
            elif self.rect.top < 0:
                self.setdirection("downleft")
            elif self.rect.left < 0:
                self.setdirection("upright")

        elif self.direction == "downleft":
            self.rect =  self.rect.move(-self.speed*interval,+self.speed*interval)
            #Two possible collisions are bottom & left (or corner)
            if self.rect.bottom > self.screenheight and self.rect.left < 0:
                self.setdirection("upright")
            elif self.rect.bottom > self.screenheight:
                self.setdirection("upleft")
            elif self.rect.left < 0:
                self.setdirection("downright")

        elif self.direction == "upright":
            self.rect =  self.rect.move(self.speed*interval,-self.speed*interval)
            #Two possible collisions are top & right (or corner)
            if self.rect.top < 0 and self.rect.right > self.screenwidth:
                self.setdirection("downleft")
            elif self.rect.top < 0:
                self.setdirection("downright")
            elif self.rect.right > self.screenwidth:
                self.setdirection("upleft")

        elif self.direction == "downright":
            self.rect =  self.rect.move(self.speed*interval,self.speed*interval)
            #Two possible collisions are bottom & right (or corner)
            if self.rect.bottom > self.screenheight and self.rect.right > self.screenwidth:
                self.setdirection("upleft")
            elif self.rect.bottom > self.screenheight:
                self.setdirection("upright")
            elif self.rect.right > self.screenwidth:
                self.setdirection("downleft")

        elif self.direction == "right":
            self.rect =  self.rect.move(self.speed*interval,0)
            #Only possible collision is to the right
            if self.rect.right > self.screenwidth:
                self.setdirection("left")

        elif self.direction == "up":
            self.rect =  self.rect.move(0,-self.speed*interval)
            #Only possible collision is top
            if self.rect.top < 0:
                self.setdirection("down")

        elif self.direction == "down":
            self.rect =  self.rect.move(0,self.speed*interval)
            #Only possible collision is bottom
            if self.rect.bottom > self.screenheight:
                self.setdirection("up")

        elif self.direction == "left":
            self.rect =  self.rect.move(-self.speed*interval,0)
            #Only possible collision is left
            if self.rect.left < 0:
                self.setdirection("right")

    #method to set the direction
    def setdirection(self, direction):
        self.direction=direction
        #set the image based on the direction
        if (direction == "right"):
            self.image = enemy.right
        elif (direction == "downright"):
            self.image = enemy.downright
        elif (direction == "down"):
            self.image = enemy.down
        elif (direction == "downleft"):
            self.image = enemy.downleft
        elif (direction == "left"):
            self.image = enemy.left
        elif (direction == "upleft"):
            self.image = enemy.upleft
        elif (direction == "up"):
            self.image = enemy.up
        elif (direction == "upright"):
            self.image = enemy.upright

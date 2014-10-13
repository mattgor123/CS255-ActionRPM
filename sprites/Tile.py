import pygame as PG


class Tile(PG.sprite.Sprite):

    HEIGHT = 10
    WIDTH = 10

    def __init__(self, collidable, x, y):
        PG.sprite.Sprite.__init__(self)
        self.collidable = collidable
        self.x = x
        self.y = y

    def isCollidable(self):
        return self.collidable

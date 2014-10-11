import pygame as PG


class Tile(PG.sprite.Sprite):

    HEIGHT = 10
    WIDTH = 10

    def __init__(self, collidable):
        self.collidable = collidable

    def isCollidable(self):
        return self.collidable
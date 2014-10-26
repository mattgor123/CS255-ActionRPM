import pygame as PG


class Tile(PG.sprite.Sprite):

    HEIGHT = 50
    WIDTH = 50

    def __init__(self, strength):
        PG.sprite.Sprite.__init__(self)
        self.strength = strength

    def get_strength(self):
        return self.strength

    def set_strength(self, new_strength):
        self.strength = new_strength

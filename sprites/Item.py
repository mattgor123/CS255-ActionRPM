import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, strength, points):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.is_collected = False
        self.strength = strength
        self.points = points

    def collect(self):
        self.is_collected = True
        pygame.sprite.Sprite.kill(self)

    def is_collectable(self):
        return True

    def get_strength(self):
        return self.strength

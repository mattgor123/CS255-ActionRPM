import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, strength, points, collectable):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.is_collected = False
        self.strength = strength
        self.points = points
        self.collectable = collectable

    def collect(self):
        self.is_collected = True
        pygame.sprite.Sprite.kill(self)

    def is_collectable(self):
        return self.collectable

    def get_strength(self):
        return self.strength

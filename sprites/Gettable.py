import pygame


class Gettable(pygame.sprite.Sprite):
    has_been_gotten = False
    name = ""

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.has_been_gotten = False
        self.name = name

    def get(self):
        self.has_been_gotten = True

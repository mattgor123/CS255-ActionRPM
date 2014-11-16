import pygame

import Item


class EZPass(Item.Item):
    pass_img = None

    def __init__(self, name, x, y):
        Item.Item.__init__(self, name, 0, 200, True)
        if EZPass.pass_img is None:
            EZPass.pass_img = pygame.image.load(
                "images/sprites/ez_pass.png").convert_alpha()
        self.image = EZPass.pass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def collect(self):
        Item.Item.collect(self)

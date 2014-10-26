import Item
import pygame


class EZPass(Item.Item):
    pass_img = None

    def __init__(self, name, x, y):
        Item.Item.__init__(self, name, 0)
        if EZPass.pass_img is None:
            EZPass.pass_img = pygame.image.load(
                "images/sprites/ez_pass.png").convert_alpha()
        self.image = EZPass.pass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.collected = False

    def collect(self):
        self.collected = True
        Item.Item.collect(self)
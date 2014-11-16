import Item
import pygame

class HealthPack(Item.Item):

    IMAGE = None

    def __init__(self, x, y):
        super(HealthPack, self).__init__("healthpack", 0, 20, True)
        if HealthPack.IMAGE is None:
            HealthPack.IMAGE = pygame.image.load(
                "images/sprites/healthpack.png").convert_alpha()
        self.image = HealthPack.IMAGE
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
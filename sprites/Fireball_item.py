import Item
import pygame


class Fireball_item(Item.Item):

    Image = None

    def __init__(self, x, y):
        Item.Item.__init__(self, "fireball", 0, 200, True)
        if Fireball_item.Image is None:
            Fireball_item.Image = \
                pygame.image.load("images/sprites/fireball.png").convert_alpha()
        self.rect = Fireball_item.Image.get_rect()
        self.image = Fireball_item.Image
        self.x = x
        self.y = y
import pygame
import Tile


class Street(Tile.Tile):
    street_img = None

    def __init__(self, x, y):
        Tile.Tile.__init__(self, 0)

        # initialize street image
        if Street.street_img is None:
            Street.street_img = pygame.image.load(
                "images/sprites/street/w_street.png").convert_alpha()
        self.image = Street.street_img
        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 's'

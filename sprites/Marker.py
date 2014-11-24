import pygame
import Item


class Marker(Item.Item):
    marker_img = None
    big_marker = None

    def __init__(self, name, x, y, pickup):
        Item.Item.__init__(self, name, 0, 0, pickup)
        if Marker.marker_img is None:
            Marker.marker_img = pygame.image.load(
                "images/sprites/marker.png").convert_alpha()
            Marker.big_marker = pygame.image.load(
                "images/sprites/big_marker.png").convert_alpha()
        if pickup:
            self.image = Marker.big_marker
        else:
            self.image = Marker.marker_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def collect(self):
        Item.Item.collect(self)

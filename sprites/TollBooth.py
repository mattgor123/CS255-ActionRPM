import Openable
import pygame


class TollBooth(Openable.Openable):
    booth_closed = None
    booth_opened = None

    def __init__(self, x, y):
        Openable.Openable.__init__(self, x, y, 0)
        if TollBooth.booth_closed is None:
            TollBooth.booth_closed = pygame.image.load(
                "images/sprites/wall/toll_booth_closed.png").convert_alpha()
        if TollBooth.booth_opened is None:
            TollBooth.booth_opened = pygame.image.load(
                "images/sprites/wall/toll_booth_opened.png").convert_alpha()
        self.image = TollBooth.booth_closed
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def open(self):
        self.image = TollBooth.booth_opened
        Openable.Openable.open(self)

    def __str__(self):
        return 't'

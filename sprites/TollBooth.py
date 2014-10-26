import Openable
import pygame


class TollBooth(Openable.Openable):
    booth_img = None

    def __init__(self, x, y):
        Openable.Openable.__init__(self, x, y, 0)
        if TollBooth.booth_img is None:
            TollBooth.booth_img = pygame.image.load(
                "images/sprites/wall/toll_booth.png").convert_alpha()
        self.image = TollBooth.pass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def open(self):
        super.open()

    def __str__(self):
        return 'o'

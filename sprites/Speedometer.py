import pygame as PG
import pygame.image as PI
import pygame.gfxdraw as PD
from states.Constants import Constants


class Speedometer(PG.sprite.Sprite):

    IMAGE = None

    def __init__(self):

        PG.sprite.Sprite.__init__(self)
        if Speedometer.IMAGE is None:
            Speedometer.IMAGE = \
                PI.load("images/speedometer.png").convert()
            Speedometer.IMAGE.set_colorkey((255, 255, 255))

        self.image = Speedometer.IMAGE
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.HEIGHT)

    def update(self, speed):
        PD.filled_circle(self.image, self.rect.center[0], self.rect.center[
            1], 20, (0, 0, 0))


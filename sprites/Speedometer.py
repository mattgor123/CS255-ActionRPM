import pygame as PG
import pygame.image as PI
import pygame.gfxdraw as PD
from states.Constants import Constants
import math


class Speedometer(PG.sprite.Sprite):

    IMAGE = None
    RED = (194, 18, 0)
    RAD = 45

    def __init__(self):

        PG.sprite.Sprite.__init__(self)
        if Speedometer.IMAGE is None:
            Speedometer.IMAGE = \
                PI.load("images/speedometer3.png").convert()
            Speedometer.IMAGE.set_colorkey((0, 0, 0))

        self.image = Speedometer.IMAGE
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.HEIGHT)
        PD.filled_circle(Speedometer.IMAGE, self.image.get_width() / 2,
                         self.image.get_height() / 2, 8, Speedometer.RED)
        self.speed = 0

    def update(self, speed):
        angle_range = 180.0
        speed_range = Constants.PLAYER_MAX_SPEED - Constants.PLAYER_MIN_SPEED
        ang_per_mil = angle_range / speed_range
        end_x = (self.image.get_width() / 2) - (Speedometer.RAD * math.cos(
            math.degrees((speed * ang_per_mil))))
        end_y = (self.image.get_height() / 2) - (Speedometer.RAD * math.sin(
            math.degrees((speed * ang_per_mil))))
        new = Speedometer.IMAGE.copy()
        PD.line(new, self.image.get_width() / 2,
                self.image.get_height() / 2, int(end_x), int(end_y),
                Speedometer.RED)
        self.image = new




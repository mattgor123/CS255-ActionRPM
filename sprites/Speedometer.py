import pygame as PG
import pygame.image as PI
import pygame.gfxdraw as PD
from states.Constants import Constants
import math


class Speedometer(PG.sprite.Sprite):
    IMAGE = None
    RED = (194, 18, 0)
    RAD = 45
    NEEDLE = None

    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        if Speedometer.IMAGE is None:
            Speedometer.IMAGE = \
                PI.load("images/sprites/speedometer/speedometer3.png")\
                       .convert()
            Speedometer.IMAGE.set_colorkey((0, 0, 0))
            Speedometer.NEEDLE = PI.load(
                "images/sprites/speedometer/needle2.png").convert_alpha()

        self.image = Speedometer.IMAGE
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.HEIGHT)
        PD.filled_circle(Speedometer.IMAGE, self.image.get_width() / 2,
                         self.image.get_height() / 2, 8, Speedometer.RED)
        self.speed = 0
        self.needle = PI.load(
            "images/sprites/speedometer/needle2.png").convert_alpha()
        self.needle.get_rect(center=self.rect.center)
        Speedometer.NEEDLE.get_rect().center = self.rect.center

    def update(self, speed):
        angle_range = 180.0  # range of motion of speedometer
        speed_range = Constants.PLAYER_MAX_SPEED - Constants.PLAYER_MIN_SPEED
        ang_per_mil = angle_range / speed_range  # Angles per Mph
        angles = -(speed * ang_per_mil) + 135  # Angles to rotate
        new = Speedometer.IMAGE.copy()
        self.needle = PG.transform.rotate(
            Speedometer.NEEDLE, angles)

        new.blit(self.needle, self.needle.get_rect(center=
                                                   Speedometer.NEEDLE
                                                   .get_rect().center))
        self.image = new

import pygame as PG

import pygame.image as PI
import pygame.gfxdraw as PD

from states.Constants import Constants


class Speedometer(PG.sprite.Sprite):
    IMAGE = None
    RED = (194, 18, 0)
    RAD = 45
    NEEDLE = None

    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        if Speedometer.IMAGE is None:
            Speedometer.IMAGE = \
                PI.load("images/sprites/hud/speed_dial.png").convert()
            Speedometer.IMAGE.set_colorkey((0, 0, 0))
            Speedometer.NEEDLE = PI.load(
                "images/sprites/hud/needle.png").convert_alpha()

        self.image = Speedometer.IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        PD.filled_circle(Speedometer.IMAGE, self.image.get_width() / 2,
                         self.image.get_height() / 2, 8, Speedometer.RED)
        self.speed = 0
        self.needle = Speedometer.NEEDLE
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

        new.blit(self.needle, self.needle.get_rect(center=Speedometer.NEEDLE
                                                   .get_rect().center))
        self.image = new

    def vol_update(self, vol):
        angle_range = 270.0
        vol_range = 1
        ang_per_mil = angle_range / vol_range
        angles = -(vol * ang_per_mil) + 135
        new = Speedometer.IMAGE.copy()
        self.needle = PG.transform.rotate(Speedometer.NEEDLE, angles)
        new.blit(self.needle, self.needle.get_rect(center=Speedometer.NEEDLE.get_rect().center))
        self.image = new
import pygame as PG
from states import Constants
import Speedometer
import Radio

class HUD():

    def __init__(self):
        self.image = PG.Surface((Constants.Constants.WIDTH, 150))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.Constants.HEIGHT)
        self.image.fill((0, 0, 0,))
        self.speedometer = Speedometer.Speedometer()
        self.radio = PG.sprite.Group()
        self.radio.add(Radio.Radio())

    def draw(self, screen):
        self.image.blit(self.speedometer.image, self.speedometer.rect)
        screen.blit(self.image, self.rect)

    def clear(self, screen):
        self.image.fill((0, 0, 0))
        screen.blit(self.image, self.rect)

    def update(self, speed):
        self.speedometer.update(speed)
        self.radio.update()

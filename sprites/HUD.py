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
        self.radio = Radio.Radio()

    def draw(self, screen):
        self.image.blit(self.speedometer.image, self.speedometer.rect)
        self.image.blit(self.radio.image, self.radio.rect)
        self.image.blit(self.radio.label.image, self.radio.text_rect)
        screen.blit(self.image, self.rect)

    def clear(self, screen):
        self.image.fill((0, 0, 0))
        screen.blit(self.image, self.rect)

    def update(self, player):
        self.speedometer.update(player.speed)
        self.radio.update()

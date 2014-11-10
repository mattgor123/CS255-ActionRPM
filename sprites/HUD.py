import pygame as PG
from states.Constants import Constants
import Speedometer
import Radio
import Label


class HUD():

    def __init__(self):
        self.image = PG.Surface((Constants.WIDTH, 150))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.HEIGHT)
        self.image.fill((0, 0, 0,))
        self.speedometer = Speedometer.Speedometer()
        self.radio = Radio.Radio()
        self.health = Label.Label("health", "Health: 100%", (650, 10))
        self.score = Label.Label("score", "Score: ", (650, 34))

    def draw(self, screen):
        self.image.blit(self.speedometer.image, self.speedometer.rect)
        self.image.blit(self.radio.image, self.radio.rect)
        self.image.blit(self.radio.label.image, self.radio.text_rect)
        self.image.blit(self.health.image, self.health.rect)
        self.image.blit(self.score.image, self.score.rect)
        screen.blit(self.image, self.rect)

    def clear(self, screen):
        self.image.fill((0, 0, 0))
        screen.blit(self.image, self.rect)

    def update(self, player, time, score):
        self.speedometer.update(player.speed)
        self.radio.update()
        self.update_labels(player, time, score)

    def update_labels(self, player, time, score):
        self.health.update(player.health)
        self.score.update(score)

import pygame as PG

from states.Constants import Constants
import Speedometer
import Radio
import Label


class HUD(PG.sprite.Sprite):
    dashboard = None

    # TODO : Add an inventory! And if possible a Mini-map
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = PG.Surface((Constants.WIDTH, 150))
        self.background = PG.Surface((Constants.WIDTH, 150))
        self.background.fill((0, 0, 0))
        self.back_rect = self.background.get_rect()
        self.back_rect.topleft = (0, 0)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Constants.HEIGHT)
        if HUD.dashboard is None:
            HUD.dashboard = PG.image.load(
                "images/sprites/hud/dashboard.png").convert_alpha()
        # self.image = HUD.dashboard
        self.all_sprites = PG.sprite.Group()
        self.speedometer = Speedometer.Speedometer()
        self.radio = Radio.Radio()
        self.health = Label.Label("health", "Health: 100%", (650, 10))
        self.score = Label.Label("score", "Score: ", (650, 34))

    def draw(self, screen, background):
        self.image.blit(HUD.dashboard, self.back_rect)
        self.image.blit(self.speedometer.image, self.speedometer.rect)
        self.image.blit(self.radio.label.image, self.radio.text_rect)
        self.image.blit(self.health.image, self.health.rect)
        self.image.blit(self.score.image, self.score.rect)
        screen.blit(self.image, self.rect)

    def clear(self, screen):
        self.image.blit(self.background, self.back_rect)

    def update(self, player, time, score):
        self.speedometer.update(player.speed)
        self.radio.update()
        self.update_labels(player, time, score)

    def update_labels(self, player, time, score):
        self.health.update(player.health)
        self.score.update(score)

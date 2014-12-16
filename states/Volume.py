import pygame
import pygame.display as display
import Menu
import State
from Constants import Constants
import sprites.Speedometer as Speedometer


# This is the state for the Title screen
class Volume(State.State):
    NUM_STEPS = 400
    image = None

    #Code to initialize a new title screen instance
    def __init__(self):
        super(Volume, self).__init__()
        self.speedometer = Speedometer.Speedometer()
        if Volume.image is None:
            Volume.image = pygame.image.load("images/volume_background.jpg")
        self.font = pygame.font.Font(None, Constants.HEIGHT / 10)
        self.text = self.font.render("Volume Slider", True, (255, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (Constants.WIDTH / 3, Constants.HEIGHT / 4)
        self.speedometer.rect.center = (Constants.WIDTH / 2, Constants.HEIGHT / 2)

    def update(self, time):
        self.speedometer.vol_update(Constants.VOLUME)

    def draw(self):
        Constants.SCREEN.fill((0, 0, 0))
        Constants.SCREEN.blit(Volume.image,
                              Volume.image.get_rect(center=(Constants.WIDTH / 2, Constants.HEIGHT / 2)))
        Constants.SCREEN.blit(self.text, self.text_rect)
        Constants.SCREEN.blit(self.speedometer.image, self.speedometer.rect)
        display.update()

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            Constants.VOLUME -= 0.05
            if Constants.VOLUME < 0:
                Constants.VOLUME = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            Constants.VOLUME += 0.05
            if Constants.VOLUME > 1:
                Constants.VOLUME = 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Constants.STATE = Menu.Menu()

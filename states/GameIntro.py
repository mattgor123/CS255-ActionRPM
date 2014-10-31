import pygame
import pygame.display as display
import Level_1
import State
from Constants import Constants


# This is the state for playing the game
class GameIntro(State.State):
    images = None
    delay = 500

    # Code to initialize a new game instance
    def __init__(self):
        State.State.__init__(self)
        Constants.SCREEN.fill(pygame.Color("black"))
        if GameIntro.images is None:
            GameIntro.images = []
            GameIntro.images.append(pygame.image.load(
                "images/screens/kicked_out.png"))
            GameIntro.images.append(pygame.image.load(
                "images/screens/never_let_down.png"))
            GameIntro.images.append(pygame.image.load(
                "images/screens/instructions.png"))
        self.current_display = 0
        self.rect = GameIntro.images[0].get_rect()
        Constants.SCREEN.blit(GameIntro.images[0], self.rect)
        self.timer = 0
        display.update()

    #Function to draw the sprite groups
    def draw(self):
        if self.timer >= GameIntro.delay:
            self.timer = 0
            if self.current_display == 2:
                Constants.STATE = Level_1.Level_1()
            else:
                self.current_display += 1
                Constants.SCREEN.fill(pygame.Color("black"))
                Constants.SCREEN.blit(GameIntro.images[self.current_display],
                                      self.rect)
                display.update()
        else:
            pass

    #Function for key updates
    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.timer = GameIntro.delay

    def update(self, time):
        self.timer += 1

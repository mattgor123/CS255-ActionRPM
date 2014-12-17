import pygame

import pygame.display as display

import State

# from Play import Play
from Constants import Constants


# This is the state for playing the game
class Level_3_Cutscene(State.State):
    images = None
    delay = 500

    # Code to initialize a new game instance
    def __init__(self):
        State.State.__init__(self)
        Constants.SCREEN.fill(pygame.Color("black"))
        if Level_3_Cutscene.images is None:
            Level_3_Cutscene.images = []
            Level_3_Cutscene.images.append(pygame.image.load(
                "images/screens/level_3_cutscene_1.jpg"))
            Level_3_Cutscene.images.append(pygame.image.load(
                "images/screens/level_3_cutscene_2.jpg"))
            Level_3_Cutscene.images.append(pygame.image.load(
                "images/screens/level_3_cutscene_3.jpg"))
            Level_3_Cutscene.images.append(pygame.image.load(
                "images/screens/level_3_cutscene_4.jpg"))
            Level_3_Cutscene.images.append(pygame.image.load(
                "images/screens/level_3_cutscene_5.jpg"))
        self.current_display = 0
        self.rect = Level_3_Cutscene.images[0].get_rect()
        Constants.SCREEN.blit(Level_3_Cutscene.images[0], self.rect)
        self.timer = 0
        display.update()

    #Function to draw the sprite groups
    def draw(self):
        if self.timer >= Level_3_Cutscene.delay:
            self.timer = 0
            if self.current_display == 4:
                # Constants.Levels = []
                # Constants.Levels.append(None)
                # Constants.Levels.append(None)
                # Constants.Levels[0] = Level_1.Level_1()
                Constants.STATE = Constants.PLAY
                #Go to 3rd level
                Constants.STATE.set_level(3)
            else:
                self.current_display += 1
                Constants.SCREEN.fill(pygame.Color("black"))
                Constants.SCREEN.blit(
                    Level_3_Cutscene.images[self.current_display],
                    self.rect)

                alphaSurface = pygame.Surface((Constants.WIDTH,Constants.HEIGHT)) # The custom-surface of the size of the screen.
                alphaSurface.fill((0,0,0))
                alphaSurface.set_alpha(Constants.ALPHA_SURFACE) # Set the incremented alpha-value to the custom surface.
                Constants.SCREEN.blit(alphaSurface,(0,0))

                display.update()
        else:
            pass

            #Function for key updates

    def keyEvent(self, event):
            if event.type == pygame.KEYDOWN:
                self.timer = Level_3_Cutscene.delay

    def update(self, time):
        self.timer += 1

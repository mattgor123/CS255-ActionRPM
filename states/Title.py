import pygame
import pygame.display as display
import Play
import State
from Constants import Constants


#This is the state for the Title screen
class Title(State.State):
    NUM_STEPS = 400
    image = None

    #Code to initialize a new title screen instance
    def __init__(self):
        super(Title, self).__init__()
        if (Title.image is None):
            Title.image = pygame.image.load("images/action_rpm_title_car.png")
        self.image = Title.image
        self.steps = 0
        self.num_steps = Title.NUM_STEPS
        self.rect = self.image.get_rect()
        self.speed = (Constants.WIDTH) / Title.NUM_STEPS
        self.font = pygame.font.Font(None, 150)

    def update(self, time):
        self.steps += 1

    def draw(self):
        #Animate the car until we want a 'trail' of fire
        if self.steps * self.speed <= Constants.WIDTH:
            Constants.SCREEN.fill((0, 0, 0))
            #Center our 'Press any key text'
            font = pygame.font.Font(None, 30)
            presskey = font.render("Press any key to continue", 1, (255,
                                                                   255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            presskeyrect = presskey.get_rect()
            presskeyrect.centerx = background.get_rect().centerx
            presskeyrect.y = Constants.HEIGHT - 40
            Constants.SCREEN.blit(presskey, presskeyrect)
        #Move the car until it's off the screen
        if self.rect.left <= Constants.WIDTH:
            self.rect.midright = (self.steps * self.speed, Constants.HEIGHT
                                  / 2)
            Constants.SCREEN.blit(self.image, self.rect)
        #Once it's off the screen, show our ActionRPM text
        else:
            label = self.font.render("ActionRPM", 1, (0, 0, 0))
            Constants.SCREEN.blit(label, (Constants.WIDTH / 3.5,
                                          Constants.HEIGHT / 3))
        display.update()

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
            Constants.STATE = Play.Play()

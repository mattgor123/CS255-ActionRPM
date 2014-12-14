import pygame
import pygame.display as display
import State
import Menu
from Constants import Constants


# This is the state for the HighScore screen
class GameEnded(State.State):
    dis_text = None

    # Code to initialize a new title screen instance
    def __init__(self, text):
        self.dis_text = text
        self.drawn = False
        super(GameEnded, self).__init__()
        self.title_font = pygame.font.Font(None, Constants.HEIGHT * 3 / 15)
        if pygame.mixer is not None:
            pygame.mixer.music.pause()

    def update(self, time):
        pass

    def draw(self):
        if self.drawn is False:
            Constants.SCREEN.fill((0, 0, 0))
            game_ended = self.title_font.render(self.dis_text, 1,
                                                (255, 255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            game_ended_rect = game_ended.get_rect()
            game_ended_rect.center = background.get_rect().center
            Constants.SCREEN.blit(game_ended, game_ended_rect)
            # Center our 'Press any key text'
            font = pygame.font.Font(None, 30)
            presskey = font.render("Press the ESC key to quit, or (m) "
                                   "to go back to the Menu", 1,
                                   (255, 255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            presskeyrect = presskey.get_rect()
            presskeyrect.centerx = background.get_rect().centerx
            presskeyrect.y = Constants.HEIGHT - 40
            Constants.SCREEN.blit(presskey, presskeyrect)

            alphaSurface = pygame.Surface((Constants.WIDTH,Constants.HEIGHT)) # The custom-surface of the size of the screen.
            alphaSurface.fill((0,0,0))
            alphaSurface.set_alpha(Constants.ALPHA_SURFACE) # Set the incremented alpha-value to the custom surface.
            Constants.SCREEN.blit(alphaSurface,(0,0))

            display.update()
            self.drawn = True
        else:
            pass

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_m:
                Constants.STATE = Menu.Menu()

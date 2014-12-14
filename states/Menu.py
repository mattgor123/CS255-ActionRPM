import pygame
import pygame.display as display
import State
import GameIntro
import HighScore
from Constants import Constants


# This is the state for playing the game
class Menu(State.State):
    image = None

    # Code to initialize a new game instance
    def __init__(self):
        State.State.__init__(self)
        Constants.SCREEN.fill(pygame.Color("black"))
        self.menu_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, Constants.WIDTH / 30)
        self.selected = 0
        self.moved = True
        # TODO : Make this shit not suck (aka organize our code a bit)
        if pygame.mixer is not None:
            pygame.mixer.music.pause()
        if Menu.image is None:
            Menu.image = pygame.image.load("images/action_rpm_title_car.png")
        self.image = Menu.image

    # Function to draw the sprite groups
    def draw(self):
        if self.moved:
            Constants.SCREEN.fill((0, 0, 0))
            self.play_color, self.adjustv_color, self.adjusta_color, \
                self.high_color, self.quit_color, self.text_color = \
                ((255, 255, 255),) * 6

            if (self.selected == 0):
                self.play_color = (255, 255, 0)
            elif self.selected == 1:
                self.adjustv_color = (255, 255, 0)
            elif self.selected == 2:
                self.adjusta_color = (255, 255, 0)
            elif self.selected == 3:
                self.high_color = (255, 255, 0)
            elif self.selected == 4:
                self.quit_color = (255, 255, 0)

            image_rect = self.image.get_rect()
            text = self.text_font.render("Use the arrow keys to select an "
                                         "option. 'Ctrl + M' will return you "
                                         "to the menu at any time.",
                                         1, self.text_color)
            self.main_font = pygame.font.Font(None, Constants.HEIGHT / 5)
            menu_text = self.main_font.render("Main Menu", 1, self.text_color)
            menu_text_rect = menu_text.get_rect()
            text_rect = text.get_rect()
            background = pygame.Surface(Constants.SCREEN.get_size())
            image_rect.centerx = background.get_rect().centerx
            text_rect.centerx = background.get_rect().centerx
            text_rect.top = Constants.HEIGHT / 50
            image_rect.top = text_rect.top + Constants.HEIGHT / 100
            menu_text_rect.centery = image_rect.centery
            menu_text_rect.centerx = image_rect.centerx
            Constants.SCREEN.blit(self.image, image_rect)
            Constants.SCREEN.blit(menu_text, menu_text_rect)
            Constants.SCREEN.blit(text, text_rect)
            #Using the title font, render the title Menu Screen
            play = self.menu_font.render("Play", True, self.play_color)
            adjustV = self.menu_font.render("Adjust Visual Brightness", True,
                                            self.adjustv_color)
            adjustA = self.menu_font.render("Adjust Audio Volume", True,
                                            self.adjusta_color)
            high_scores = self.menu_font.render("High Scores", True,
                                                self.high_color)
            quit_game = self.menu_font.render("Quit", True, self.quit_color)

            playwidth, playheight = play.get_size()
            adjust_v_width, adjust_v_height = adjustV.get_size()
            adjust_a_width, adjust_a_height = adjustA.get_size()
            hs_width, hs_height = high_scores.get_size()
            quit_width, quit_height = quit_game.get_size()

            Constants.SCREEN.blit(play, (Constants.WIDTH / 2 - playwidth / 2,
                                         Constants.HEIGHT / 2 - playheight /
                                         2 + 40))
            Constants.SCREEN.blit(adjustV,
                                  (Constants.WIDTH / 2 - adjust_v_width / 2,
                                   Constants.HEIGHT / 2 - adjust_v_height / 2 +
                                   90))
            Constants.SCREEN.blit(adjustA,
                                  (Constants.WIDTH / 2 - adjust_a_width / 2,
                                   Constants.HEIGHT / 2 - adjust_a_height / 2 +
                                   140))
            Constants.SCREEN.blit(high_scores,
                                  (Constants.WIDTH / 2 - hs_width / 2,
                                   Constants.HEIGHT / 2 - hs_height / 2 + 190))
            Constants.SCREEN.blit(quit_game,
                                  (Constants.WIDTH / 2 - quit_width / 2,
                                   Constants.HEIGHT / 2 - quit_height / 2 +
                                   240))
            self.moved = False

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
            if (event.key == pygame.K_DOWN):
                self.moved = True
                if self.selected < 4:
                    self.selected += 1
                else:
                    self.selected = 0
            elif (event.key == pygame.K_UP):
                self.moved = True
                if (self.selected > 0):
                    self.selected -= 1
                else:
                    self.selected = 4
            elif (event.key == pygame.K_RETURN):
                change_event(self.selected)
            else:
                pass

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        pass


def change_event(selected):
    if (selected == 0):
        Constants.STATE = GameIntro.GameIntro()
    elif (selected == 1):
        if Constants.ALPHA_SURFACE > 80:
            Constants.ALPHA_SURFACE = 0
            Constants.STATE.moved = True
            Constants.STATE.draw()
        else:
            Constants.ALPHA_SURFACE += 30
            Constants.STATE.moved = True
            Constants.STATE.draw()
    elif (selected == 3):
        Constants.STATE = HighScore.HighScore("", 0, False)
    elif (selected == 4):
        exit()

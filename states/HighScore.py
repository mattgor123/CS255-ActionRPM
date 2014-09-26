import pygame
import pygame.display as display
import Menu
import State
import pickle
from Constants import Constants


# This is the state for the HighScore screen
class HighScore(State.State):
    # Code to initialize a new title screen instance
    def __init__(self, name, score, from_new):
        super(HighScore, self).__init__()
        self.title_font = pygame.font.Font(None, Constants.WIDTH / 7)
        self.score_font = pygame.font.Font(None, Constants.WIDTH / 16)
        # Code to read the high scores (adapted from http://bit.ly/YegHuS
        f = open(Constants.HIGH_SCORE_FILE, "rb")
        try:
            self.scores = pickle.load(f)
        except:
            self.scores = []
        f.close()
        self.drawn = False
        self.from_new = False
        self.score = score
        self.name = name
        self.from_new = from_new

    def update(self, time):
        pass

    def draw(self):
        if (self.drawn == False):
            Constants.SCREEN.fill((0, 0, 0))
            high_title = self.title_font.render("Your High Scores", 1,
                                                (255, 255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            high_title_rect = high_title.get_rect()
            high_title_rect.centerx = background.get_rect().centerx
            high_title_rect.centery = 75
            Constants.SCREEN.blit(high_title, high_title_rect)
            # Center our 'Press any key text'
            font = pygame.font.Font(None, 30)
            presskey = font.render("Press any key to get back to the Menu, "
                                   "or the ESC key to quit", 1,
                                   (255, 255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            presskeyrect = presskey.get_rect()
            presskeyrect.centerx = background.get_rect().centerx
            presskeyrect.y = Constants.HEIGHT - 40
            Constants.SCREEN.blit(presskey, presskeyrect)

            if len(self.scores) == 0:
                score = self.score_font.render("No high scores yet!", 1,
                                               (255, 255, 255))
                score_rect = score.get_rect()
                score_rect.centerx = background.get_rect().centerx
                score_rect.y = high_title_rect.bottom + 100
                Constants.SCREEN.blit(score, score_rect)
            else:
                rect_top = high_title_rect.bottom + Constants.HEIGHT / 100
                rect_left = high_title_rect.left + Constants.WIDTH / 40
                for i in range(len(self.scores)):
                    color = (255, 0, 0)
                    curr_name = self.scores[i][0]
                    curr_score = self.scores[i][1]
                    if (self.from_new):
                        if (self.name == curr_name):
                            if (abs(self.score - curr_score) < .01):
                                color = (0, 255, 0)
                    curr_score = self.score_font.render(
                        str(i + 1) + ". " + self.scores[i][0] + ": " +
                        "%3.2f" % self.scores[i][1], 1, color)
                    curr_score_rect = curr_score.get_rect()
                    curr_score_rect.left = rect_left
                    curr_score_rect.top = rect_top
                    Constants.SCREEN.blit(curr_score, curr_score_rect)
                    rect_top += Constants.WIDTH / 20

            display.update()
            self.drawn = True
        else:
            pass

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            else:
                Constants.STATE = Menu.Menu()

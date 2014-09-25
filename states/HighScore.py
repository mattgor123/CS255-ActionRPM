import pygame
import pygame.display as display
import Play
import State
import pickle
from Constants import Constants


#This is the state for the Title screen
class HighScore(State.State):

    #Code to initialize a new title screen instance
    def __init__(self):
        super(HighScore, self).__init__()
        self.title_font = pygame.font.Font(None, Constants.WIDTH / 7)
        self.score_font = pygame.font.Font(None, Constants.WIDTH / 16)
        #Code to read the high scores (adapted from http://bit.ly/YegHuS
        f = open(Constants.HIGH_SCORE_FILE, "rb")
        try:
            self.scores = pickle.load(f)
        except:
            self.scores = []
        f.close()
        self.drawn = False


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
            #Center our 'Press any key text'
            font = pygame.font.Font(None, 30)
            presskey = font.render("Press any key to continue", 1, (255,
                                                                   255, 255))
            background = pygame.Surface(Constants.SCREEN.get_size())
            presskeyrect = presskey.get_rect()
            presskeyrect.centerx = background.get_rect().centerx
            presskeyrect.y = Constants.HEIGHT - 40
            Constants.SCREEN.blit(presskey, presskeyrect)

            if len(self.scores) == 0:
                score = self.score_font.render("No high scores yet!",1,
                                                  (255, 255, 255))
                score_rect = score.get_rect()
                score_rect.centerx = background.get_rect().centerx
                score_rect.y = high_title_rect.bottom + 100
                Constants.SCREEN.blit(score, score_rect)
            else:
                rect_top = high_title_rect.bottom + Constants.HEIGHT / 100
                rect_left = background.get_rect().centerx - Constants.WIDTH /\
                                                            7
                for i in range(len(self.scores)):
                    curr_score = self.score_font.render(str(i+1) +
                                    ". " + self.scores[i][0] + ": " + "%3.2f" %
                                    self.scores[i][1], 1, (255, 0, 0))
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
        if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
            Constants.STATE = Play.Play()
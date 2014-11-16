import pygame
import pickle
import string

import pygame.display as display

import State
import HighScore
from Constants import Constants


# This is the state for adding a new high score
class NewHigh(State.State):
    # Code to initialize a new title screen instance
    def __init__(self, score):
        super(NewHigh, self).__init__()
        self.score_font = pygame.font.Font(None, Constants.WIDTH / 16)
        #Code to read the high scores (adapted from http://bit.ly/YegHuS
        f = open(Constants.HIGH_SCORE_FILE, "rb")
        try:
            self.scores = pickle.load(f)
        except:
            self.scores = []
        f.close()
        self.score = score
        self.name = []

    def update(self, time):
        pass

    def draw(self):
        Constants.SCREEN.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        new_high = font.render("Congratulations! You have a new high score", 1,
                               (255, 255, 255))
        background = pygame.Surface(Constants.SCREEN.get_size())
        new_high_rect = new_high.get_rect()
        new_high_rect.centerx = background.get_rect().centerx
        new_high_rect.centery = 75
        Constants.SCREEN.blit(new_high, new_high_rect)
        font = pygame.font.Font(None, 30)
        presskey = font.render("Please type your name, then hit 'Enter'", 1,
                               (255, 255, 255))
        background = pygame.Surface(Constants.SCREEN.get_size())
        presskeyrect = presskey.get_rect()
        presskeyrect.centerx = background.get_rect().centerx
        presskeyrect.y = Constants.HEIGHT - 40
        Constants.SCREEN.blit(presskey, presskeyrect)
        #Print a red rectangle in the middle of the screen
        rect = pygame.draw.rect(Constants.SCREEN, (255, 0, 0),
                                (0, Constants.HEIGHT / 2,
                                 Constants.WIDTH, 30))

        if len(self.name) != 0:
            name_msg = font.render(string.join(self.name, ""), 1, (0, 0, 0))
            name_msg_rect = name_msg.get_rect()
            name_msg_rect.center = rect.center
            Constants.SCREEN.blit(name_msg, name_msg_rect)
        display.flip()

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_DELETE:
                self.name = []
            elif event.key == pygame.K_BACKSPACE:
                if len(self.name) > 0:
                    self.name = self.name[0:-1]
            elif event.key == pygame.K_RETURN:
                if len(self.name) == 0:
                    self.name = "blank"
                self.name = string.join(self.name, "")
                entry = (str(self.name), self.score)
                self.scores.append(entry)
                save_scores(self)
            elif event.key <= 127:
                if len(self.name) < 20:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.name.append(string.upper(chr(event.key)))
                    else:
                        self.name.append(chr(event.key))


# Function to add a score to the list
def save_scores(self):
    self.scores.sort(key=lambda x: x[1], reverse=True)
    self.scores = self.scores[0:10]
    f = open(Constants.HIGH_SCORE_FILE, "wb")
    pickle.dump(self.scores, f)
    f.close()
    Constants.STATE = HighScore.HighScore(self.name, self.score, True)

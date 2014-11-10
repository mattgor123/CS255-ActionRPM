import State
from sprites import Player
from sprites import HUD
from sprites import Label
from Constants import Constants
import Menu
import pygame
import levels.Level_1 as Level_1


class Play(State.State):

    def __init__(self):
        self.player = Player.Player([8, 6], [Constants.WIDTH, Constants.HEIGHT])
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.hud = HUD.HUD()
        self.init_labels()
        self.background = pygame.Surface(Constants.SCREEN.get_size())
        self.levels = []
        self.current_level = 0
        self.init_levels()

    def init_levels(self):
        self.add_level(Level_1.Level_1(self.player))
        # self.add_level(Level_2.Level_2())

    def init_labels(self):
        #Make labels
        self.labels = pygame.sprite.Group()
        self.labels.add(Label.Label("health", "Health: 100%", (10, 10)))
        self.labels.add(Label.Label("score", "Score: ", (10, 34)))

    def update(self, interval):
        self.players.update(interval)
        self.hud.update(self.player)
        self.labels.update(interval)
        self.levels[self.current_level].update(interval)

    def draw(self):
        self.players.clear(Constants.SCREEN, self.background)
        self.hud.clear(Constants.SCREEN)
        self.labels.clear(Constants.SCREEN, self.background)

        self.levels[self.current_level].draw(self.background)

        self.players.draw(Constants.SCREEN)
        self.hud.draw(Constants.SCREEN)
        self.labels.draw(Constants.SCREEN)

        pygame.display.update()

    def add_level(self, level):
        self.levels.append(level)

    def set_level(self, level_num):
        self.levels[self.current_level].map = None
        old_level = self.current_level
        self.current_level = level_num
        if self.levels[self.current_level] is None:
            raise Exception
        self.player.set_coordinates(self.levels[self.current_level].PLAYER_START)
        self.levels[self.current_level].init_map()

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.game_over(False)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()

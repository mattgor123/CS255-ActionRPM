import pygame

import State
from sprites import Player
from sprites import HUD
from Constants import Constants
import Menu
import levels.Level_1 as Level_1
import levels.Level_2 as Level_2
import levels.Level_3 as Level_3
import levels.Level_4 as Level_4


class Play(State.State):
    # TODO : Let's start thinking about points mechanisms & also health & NOS??
    def __init__(self):
        super(Play, self).__init__()
        self.player = Player.Player([8, 6], [Constants.WIDTH,
                                             Constants.HEIGHT])
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.hud = HUD.HUD()
        self.background = pygame.Surface(Constants.SCREEN.get_size())
        self.levels = []
        self.current_level = 0
        self.init_levels()
        self.time = 0.00

    def init_levels(self):
        self.add_level(Level_1.Level_1(self.player))
        self.add_level(Level_2.Level_2(self.player))
        self.add_level(Level_3.Level_3(self.player))
        self.add_level(Level_4.Level_4(self.player))

    def update(self, interval):
        self.time += interval
        self.players.update(interval)
        self.hud.update(self.player, self.time, self.player.score)
        self.levels[self.current_level].update(interval)

    def draw(self):
        self.players.clear(Constants.SCREEN, self.background)
        self.hud.clear(Constants.SCREEN)

        self.levels[self.current_level].draw(self.background)

        self.players.draw(Constants.SCREEN)
        self.hud.draw(Constants.SCREEN, self.background)

        pygame.display.update()

    def add_level(self, level):
        self.levels.append(level)

    def set_level(self, level_num):
        self.levels[self.current_level].map = None
        old_level = self.current_level
        self.current_level = level_num
        if self.levels[self.current_level] is None:
            raise Exception
        self.player.set_coordinates(
            self.levels[self.current_level].PLAYER_START)
        self.levels[self.current_level].init_map()

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()
            elif event.key == pygame.K_LEFT:
                if self.hud.radio.is_on:
                    self.hud.radio.decrement_current_index_and_play()
            elif event.key == pygame.K_RIGHT:
                if self.hud.radio.is_on:
                    self.hud.radio.increment_current_index_and_play()
            elif event.key == pygame.K_KP0:
                if self.hud.radio.is_on:
                    self.hud.radio.play_random_song()
            elif event.key == pygame.K_o:
                self.hud.radio.toggle_radio()
            elif event.key == pygame.K_1:
                self.set_level(0)
            elif event.key == pygame.K_2:
                self.set_level(1)
            elif event.key == pygame.K_3:
                self.set_level(2)
        #For debugging purposes ... print where you click on screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

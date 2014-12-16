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
        #self.current_level = 0
        #self.init_levels()
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
        self.level.update(interval)

    def draw(self):
        self.players.clear(Constants.SCREEN, self.background)
        self.hud.clear(Constants.SCREEN)
        self.player.projectiles.clear(Constants.SCREEN, self.background)

        self.level.draw(self.background)

        self.players.draw(Constants.SCREEN)
        self.player.projectiles.draw(Constants.SCREEN)
        self.hud.draw(Constants.SCREEN, self.background)

        alphaSurface = pygame.Surface((Constants.WIDTH,Constants.HEIGHT)) # The custom-surface of the size of the screen.
        alphaSurface.fill((0,0,0))
        alphaSurface.set_alpha(Constants.ALPHA_SURFACE) # Set the incremented alpha-value to the custom surface.
        Constants.SCREEN.blit(alphaSurface,(0,0))

        pygame.display.update()

    def add_level(self, level):
        self.levels.append(level)

    def set_level(self, level_num):
        if level_num == 0:
            self.level = Level_1.Level_1(self.player)
        elif level_num == 1:
            self.level = Level_2.Level_2(self.player)
        elif level_num == 2:
            self.level = Level_3.Level_3(self.player)
        elif level_num == 3:
            self.level = Level_4.Level_4(self.player)
        self.player.set_coordinates(
            self.level.PLAYER_START)
        self.level.init_map()

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
            elif event.key == pygame.K_4:
                self.set_level(3)
            elif event.key == pygame.K_SPACE:
                self.player.shoot()
        elif event.type == pygame.JOYBUTTONDOWN:
            if Constants.JOYSTICK.get_button(2):
                self.player.shoot()
        #For debugging purposes ... print where you click on screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

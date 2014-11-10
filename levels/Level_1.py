from Level import Level
import pygame
import sprites.EZPass as EZPass
import sprites.Enemy as Enemy
from states.Constants import Constants
import map.Map as Map
import states.GameEnded as GameEnded


class Level_1(Level):

    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        self.init_items()
        self.tiles = None
        self.PLAYER_START = [8, 6]

    def init_items(self):
        #Create miscellaneous shit
        self.items.add(EZPass.EZPass("ezpass", 40, 19))

    def init_enemies(self):
        #Put in enemies
        #This enemy is by the EZpass exit
        self.enemies.add(Enemy.Enemy([39.2, 3.4], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d3", "r1.8", "u3", "l1.8"]))
        #This enemy is driving around the bottom of the screen
        self.enemies.add(Enemy.Enemy([40.4, 17.5],
                                [Constants.WIDTH, Constants.HEIGHT],
                                5, "down", ["d12.5", "l16", "u12.5", "r16"]))

    def update(self, interval):
        super(Level_1, self).update(interval)

    def draw(self, background):
        self.tiles.clear(Constants.SCREEN, background)
        self.tiles.draw(Constants.SCREEN)
        super(Level_1, self).draw(background)

    def set_tiles(self):
        self.tiles = self.map.render(self.player.x, self.player.y)
        self.player.rect.topleft = self.map.get_topleft(self.player.x,
                                                    self.player.y)
        for enemy in self.enemies.sprites():
            enemy.rect.topleft = self.map.get_topleft(enemy.x, enemy.y)
        for item in self.items.sprites():
            item.rect.topleft = self.map.get_topleft(item.x, item.y)

    def init_map(self):
        self.map = Map.Map("level1.txt", 3)
        self.set_tiles()

    def game_over(self, died):
        if died:
            Constants.STATE = GameEnded.GameEnded("GAME OVER")
        else:
            Constants.STATE.set_level(1)
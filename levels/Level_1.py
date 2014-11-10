"""Level 1  logic of actionRPM"""

from Level import Level
import sprites.EZPass as EZPass
import sprites.Enemy as Enemy
from states.Constants import Constants
import map.Map as Map
import states.GameEnded as GameEnded
import sprites.Label as Label
import pygame


class Level_1(Level):

    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        self.init_items()
        self.tiles = None
        self.PLAYER_START = [8, 6]
        self.is_beatable = False
        self.init_labels()

    def init_labels(self):
        self.objective_text = "Find the EZ-Pass to cross the bridge"
        self.objectives = pygame.sprite.Group()
        self.objective = Label.Label("objective", self.objective_text, (175, 175))
        self.objective.font = pygame.font.Font(None, 45)
        self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 255))
        self.objectives.add(self.objective)
        self.label_count = 0

    def check_objective(self):
        if self.label_count < 375:
            self.label_count += 1
            if self.label_count < 75:
                self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 150:
                self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 0))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 225:
                self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 300:
                self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 0))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 375:
                self.objective.image = self.objective.font.render(self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)

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
        player_coordinates = super(Level_1, self).update(interval)
        if player_coordinates[1] <= .5:
            Constants.STATE.set_level(1)

    def draw(self, background):
        self.tiles.clear(Constants.SCREEN, background)
        self.tiles.draw(Constants.SCREEN)
        self.check_objective()

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

    def enemy_collided(self, enemy, damage):
        #Do the damage as prescribed by the collided box
        self.player.damage += damage
        #If we hit an enemy, make the enemy stop
        if type(enemy) is Enemy.Enemy:
            enemy.stop()

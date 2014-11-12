from Level import Level
import sprites.Enemy as Enemy
from states.Constants import Constants
from states.GameEnded import GameEnded
import map.Map as Map
import pygame
import sprites.Label as Label


class Level_3(Level):

    def __init__(self, player):
        Level.__init__(self, player)
        #self.init_enemies()
        #self.init_items()
        self.PLAYER_START = [108, 40]
        self.is_beatable = False
        self.init_labels()

    def init_items(self):
        #Create miscellaneous shit
        pass

    def init_labels(self):
        self.objective_text = "Level Three Bitch!"
        self.objectives = pygame.sprite.Group()
        self.objective = Label.Label("objective",self.objective_text, (125, 175))
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

    def init_enemies(self):
        #Put in enemies
        #This enemy is by the EZpass exit
        self.enemies.add(Enemy.Enemy([39.2, 4.4], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d3", "r1.8", "u3", "l1.8"]))
        self.enemies.add(Enemy.Enemy([40.4, 17.5],
                                [Constants.WIDTH, Constants.HEIGHT],
                                5, "down", ["d12.5", "l16", "u12.5", "r16"]))
        self.enemies.add(Enemy.Boss_1([70, 40],
                                 [Constants.WIDTH,
                                  Constants.HEIGHT]))

    def update(self, interval):
        super(Level_3, self).update(interval)
        if self.player.x >= 111:
            Constants.STATE.set_level(1)
        #if self.player.y <= 0.5:
         #   Constants.STATE.set_level(2)

    def draw(self, background):

        super(Level_3, self).draw(background)
        self.check_objective()

    def init_map(self):
        self.map = Map.Map("level3.txt", 7)
        self.set_tiles()

    def game_over(self, died):
        if died:
            Constants.STATE = GameEnded("GAME OVER")
        else:
            Constants.STATE.set_level(1)

    def enemy_collided(self, enemy, damage):
        self.player.damage += damage
        #There should be a bigger boss class that all bosses
        #Are derived from
        if(damage == 0 and type(enemy) is Enemy.Boss_1):
            enemy.hurt(3)
            #Sets the game to game over if we kill the boss
            if enemy.get_health() == 0:
                self.game_over()
        #If we hit an enemy, make the enemy stop
        elif type(enemy) is Enemy.Enemy:
            enemy.stop()

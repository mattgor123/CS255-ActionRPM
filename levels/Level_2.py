import pygame

from Level import Level
import sprites.Enemy as Enemy
import sprites.HealthPack as HealthPack
from states.Constants import Constants
from states.GameEnded import GameEnded
import map.Map as Map
import sprites.Label as Label
import states.Level_2_Cutscene as Level_2_Cutscene


class Level_2(Level):
    # TODO : Add health packs, make it so you can't beat with just EZ Pass,
    # possibly add another cooler mechanic than beating da OG bawse
    #TODO : Make the exit leading to level 3 on the left side of the map,
    # a T rotated 90 degrees clockwise, for cohesion with level 3.
    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        self.init_items()
        self.PLAYER_START = [72, 57]
        self.is_beatable = False
        self.init_labels()

    def init_items(self):
        #Create miscellaneous shit
        self.items.add(HealthPack.HealthPack(70, 55))
        self.items.add(HealthPack.HealthPack(8, 10))
        self.items.add(HealthPack.HealthPack(30, 29))
        self.items.add(HealthPack.HealthPack(72, 17))
        self.items.add(HealthPack.HealthPack(37, 5))

    def init_labels(self):
        self.objective_text = "Wreck the boss car to win back your girl!"
        self.objectives = pygame.sprite.Group()
        self.objective = Label.Label("objective", self.objective_text, (125,
                                                                        175))
        self.objective.font = pygame.font.Font(None, 45)
        self.objective.image = self.objective.font.render(self.objective_text,
                                                          1, (255, 255, 255))
        self.objectives.add(self.objective)
        self.label_count = 0
        self.health_text = "Enemy Health: 100%"
        self.enemy_health = pygame.sprite.Group()
        self.enemy_health_label = Label.Label("enemy_health", "Enemy Health: ",
                                              (250, 20))
        self.enemy_health_label.font = pygame.font.Font(None, 35)
        self.enemy_health_label.image = self.enemy_health_label.font.render(
            "Enemy Health: ", 1, (51, 255, 51))
        self.enemy_health.add(self.enemy_health_label)

    def check_objective(self):
        if self.label_count < 525:
            self.label_count += 1
            if self.label_count < 75:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 150:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 0))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 225:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 300:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 0))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 375:
                self.objective_text = "Be careful, he likes to teleport"
                self.objectives = pygame.sprite.Group()
                self.objective = Label.Label("objective", self.objective_text,
                                             (175, 175))
                self.objective.font = pygame.font.Font(None, 45)
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 255))
                self.objectives.add(self.objective)
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 450:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 0))
                self.objectives.draw(Constants.SCREEN)
            elif self.label_count < 525:
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)

    def init_enemies(self):
        #Put in enemies
        #This enemy is by the EZpass exit
        self.enemies.add(Enemy.Enemy([39.2, 4.4], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d3", "r1.8", "u3", "l1.8"]))
        self.enemies.add(Enemy.Enemy([40.4, 17.5],
                                     [Constants.WIDTH, Constants.HEIGHT],
                                     5, "down",
                                     ["d12.5", "l16", "u12.5", "r16"]))
        self.boss = Enemy.Boss_1([8, 5],
                                 [Constants.WIDTH,
                                  Constants.HEIGHT])
        self.enemies.add(self.boss)

    def update(self, interval):
        super(Level_2, self).update(interval)
        if self.player.y >= 58:
            Constants.STATE.set_level(0)
        if self.player.y <= 0.5:
            Constants.STATE.set_level(2)

    def draw(self, background):
        super(Level_2, self).draw(background)
        self.check_objective()

        self.enemy_health.update(self.boss.get_health())
        self.enemy_health.draw(Constants.SCREEN)

    def init_map(self):
        self.map = Map.Map("level2.txt", 5)
        self.set_tiles()

    def game_over(self, died):
        if died:
            Constants.STATE = GameEnded("GAME OVER")
        else:
            Constants.STATE.set_level(2)


    def enemy_collided(self, enemy, damage):
        self.player.damage += damage
        #There should be a bigger boss class that all bosses
        #Are derived from
        if (damage == 0 and type(enemy) is Enemy.Boss_1):
            enemy.hurt(3)
            #Sets the game to our cutscene if the boss is dead
            if enemy.get_health() == 0:
                self.player.score += 500
                Constants.STATE = Level_2_Cutscene.Level_2_Cutscene()
        #If we hit an enemy, make the enemy stop
        elif type(enemy) is Enemy.Enemy:
            enemy.stop()

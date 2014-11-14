from Level import Level
import sprites.Enemy as Enemy
import sprites.Fireball as Fireball
from states.Constants import Constants
from states.GameEnded import GameEnded
import random
import map.Map as Map
import pygame
import sprites.Label as Label


class Level_3(Level):

    fireball_frequency = 200
    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        #self.init_items()
        self.PLAYER_START = [108, 40]
        self.is_beatable = False
        self.init_labels()
        self.time_between_fireballs = 0

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
        self.enemies.add(Enemy.Racer([104, 41], [
            Constants.WIDTH, Constants.HEIGHT], 8, "up",
            ["u24","l16", "d24", "l16", "d12.5", "r32", "d24", "l48",
             "u12", "l15.5", "d12", "l31.5", "u48", "r32", "u24", "r15.5",
             "d24", "r16", "u24", "r32", "d35.1" ,"p100"]))

    def shoot_fireball(self):
        for enemy in self.enemies.sprites():
            #If our racer is still alive, we can shoot a fireball
            if type(enemy) == Enemy.Racer:
                print ("shooting fireball")
                direction = enemy.direction
                i = random.randrange(0,1)
                if direction == "left":
                    if i == 0:
                        direction = "upright"
                    else:
                        direction = "downright"
                elif direction == "right":
                    if i == 0:
                        direction = "upleft"
                    else:
                        direction = "downleft"
                elif direction == "up":
                    if i == 0:
                        direction = "downleft"
                    else:
                        direction = "downright"
                elif direction == "down":
                    if i == 0:
                        direction = "upleft"
                    else:
                        direction = "upright"
                speed = random.randrange(3,7)
                duration = random.randrange(1,5) * 100
                self.enemies.add(Fireball.Fireball(speed,direction,[enemy.x,
                                                    enemy.y],duration ))



    def update(self, interval):
        super(Level_3, self).update(interval)
        if self.player.x >= 111:
            Constants.STATE.set_level(1)
        #Shoot fireballs
        self.time_between_fireballs += 1
        if (self.time_between_fireballs >= Level_3.fireball_frequency):
            self.time_between_fireballs = 0
            self.shoot_fireball()
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
        elif type(enemy) is Fireball.Fireball:
            enemy.kill()

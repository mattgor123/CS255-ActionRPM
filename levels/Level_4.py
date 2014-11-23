import random
import pygame

from Level import Level
import sprites.Enemy as Enemy
import sprites.Fireball as Fireball
import sprites.Fireball_item as Fireball_item
from states.Constants import Constants
from states.GameEnded import GameEnded
import map.Map as Map
import sprites.Label as Label
import sprites.Checkpoint as Checkpoint


class Level_4(Level):
    # TODO : Tweak difficulty / keep play testing (since I have the course
    # memorized ... I wanna know how difficult it is). Also maybe implement
    # NOS or shields or some other badass shit (down the road)
    fireball_frequency = 133

    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        self.init_items()
        self.PLAYER_START = [104, 78]
        self.is_beatable = False
        self.init_labels()
        self.time_between_fireballs = 0
        self.checkpoint = 0
        self.has_gotten_checkpoint_1 = False
        self.has_gotten_checkpoint_2 = False
        self.has_gotten_checkpoint_3 = False
        self.fireball_strength = 2
        self.timer = 0
        #Counts number of kegs the player has killed
        self.kegs = 0

    def init_items(self):
        # Create miscellaneous shit
        self.items.add(Fireball_item.Fireball_item(102, 78))

    def init_labels(self):
        self.objective_text = "Keep up with your dad's boss if you can!"
        self.objectives = pygame.sprite.Group()
        self.objective = Label.Label("objective", self.objective_text,
                                     (125, 175))
        self.objective.font = pygame.font.Font(None, 45)
        self.objective.image = self.objective.font.render(self.objective_text,
                                                          1, (255, 255, 255))
        self.objectives.add(self.objective)
        self.label_count = 0

    def check_objective(self):
        if self.label_count < 375:
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
                self.objective.image = self.objective.font.render(
                    self.objective_text, 1, (255, 255, 255))
                self.objectives.draw(Constants.SCREEN)

    def init_enemies(self):
        #First kegs you see
        self.enemies.add(Enemy.Keg([98, 72], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d20"],"ygt83"))

        self.enemies.add(Enemy.Keg([96, 83], [
            Constants.WIDTH, Constants.HEIGHT], 5.5, "up",
            ["u20"],"ylt72"))

        self.enemies.add(Enemy.Keg([94, 72], [
            Constants.WIDTH, Constants.HEIGHT], 4, "down",
            ["d20"],"ygt83"))

        self.enemies.add(Enemy.Keg([90, 83], [
            Constants.WIDTH, Constants.HEIGHT], 6, "up",
            ["u20"],"ylt72"))

        self.enemies.add(Enemy.Keg([88, 83], [
            Constants.WIDTH, Constants.HEIGHT], 5.5, "up",
            ["u20"],"ylt72"))

        self.enemies.add(Enemy.Keg([86, 83], [
            Constants.WIDTH, Constants.HEIGHT], 6.2, "up",
            ["u20"],"ylt72"))

        self.enemies.add(Enemy.Keg([4, 76], [
            Constants.WIDTH, Constants.HEIGHT], 6.2, "right",
            ["r100"],"xgt108"))
        self.enemies.add(Enemy.Keg([4, 76], [
            Constants.WIDTH, Constants.HEIGHT], 5.5, "right",
            ["r100"],"xgt108"))
        self.enemies.add(Enemy.Keg([4, 76], [
            Constants.WIDTH, Constants.HEIGHT], 5, "right",
            ["r100"],"xgt108"))
        self.enemies.add(Enemy.Keg([4, 76], [
            Constants.WIDTH, Constants.HEIGHT], 8, "right",
            ["r100"],"xgt108"))

        self.enemies.add(Enemy.Keg([4, 78], [
            Constants.WIDTH, Constants.HEIGHT], 4, "right",
            ["r100"],"xgt108"))
        self.enemies.add(Enemy.Keg([4, 78], [
            Constants.WIDTH, Constants.HEIGHT], 9, "right",
            ["r100"],"xgt108"))

        #second layer kegs
        self.enemies.add(Enemy.Keg([62, 60], [
            Constants.WIDTH, Constants.HEIGHT], 9, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([64, 70], [
            Constants.WIDTH, Constants.HEIGHT], 5, "up",
            ["u100"],"ylt60"))
        self.enemies.add(Enemy.Keg([66, 70], [
            Constants.WIDTH, Constants.HEIGHT], 7, "up",
            ["u100"],"ylt60"))

        self.enemies.add(Enemy.Keg([72, 70], [
            Constants.WIDTH, Constants.HEIGHT], 8, "up",
            ["u100"],"ylt60"))
        self.enemies.add(Enemy.Keg([74, 60], [
            Constants.WIDTH, Constants.HEIGHT], 9, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([76, 60], [
            Constants.WIDTH, Constants.HEIGHT], 7.5, "down",
            ["d100"],"ygt70"))

        self.enemies.add(Enemy.Keg([80, 60], [
            Constants.WIDTH, Constants.HEIGHT], 9, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([82, 70], [
            Constants.WIDTH, Constants.HEIGHT], 8, "up",
            ["u100"],"ylt60"))
        self.enemies.add(Enemy.Keg([84, 60], [
            Constants.WIDTH, Constants.HEIGHT], 7.5, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([87, 70], [
            Constants.WIDTH, Constants.HEIGHT], 8.5, "up",
            ["u100"],"ylt60"))

        self.enemies.add(Enemy.Keg([92, 60], [
            Constants.WIDTH, Constants.HEIGHT], 7, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([94, 70], [
            Constants.WIDTH, Constants.HEIGHT], 9, "up",
            ["u100"],"ylt60"))
        self.enemies.add(Enemy.Keg([96, 70], [
            Constants.WIDTH, Constants.HEIGHT], 10, "up",
            ["u100"],"ylt60"))
        self.enemies.add(Enemy.Keg([98, 60], [
            Constants.WIDTH, Constants.HEIGHT], 8.5, "down",
            ["d100"],"ygt70"))
        self.enemies.add(Enemy.Keg([100, 70], [
            Constants.WIDTH, Constants.HEIGHT], 9.5, "up",
            ["u100"],"ylt60"))


    def update(self, interval):
        super(Level_4, self).update(interval)

    def draw(self, background):
        super(Level_4, self).draw(background)
        self.check_objective()

    def init_map(self):
        self.map = Map.Map("level4.txt", 7)
        self.set_tiles()

    def game_over(self, died):
        if died:
            Constants.STATE = GameEnded("GAME OVER")
        else:
            Constants.STATE.set_level(1)

    def enemy_collided(self, enemy, damage):
        self.player.damage += damage
        # There should be a bigger boss class that all bosses
        #Are derived from
        if (damage == 0 and type(enemy) is Enemy.Keg):
            pass
        elif (damage == 50 and type(enemy) is Enemy.Keg):
            enemy.kill()
            self.kegs += 1

    def increment_kegs(self):
        self.kegs += 1
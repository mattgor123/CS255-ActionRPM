import random
import pygame

from Level import Level
import sprites.Enemy as Enemy
import sprites.Fireball as Fireball
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
        # self.init_items()
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

    def init_items(self):
        # Create miscellaneous shit
        pass

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
        # Also let's add checkpoints to enemies because I'm lazy
        self.enemies.add(Checkpoint.Checkpoint(1, [70, 49]))
        self.enemies.add(Checkpoint.Checkpoint(2, [11, 75]))
        self.enemies.add(Checkpoint.Checkpoint(3, [47, 3]))
        self.enemies.add(Checkpoint.Checkpoint(4, [102, 44]))
        self.enemies.add(Enemy.Racer([104, 41], [
            Constants.WIDTH, Constants.HEIGHT], 6, "up",
            ["u24", "l16", "d24", "l16", "d12.5",
             "r32", "d24", "l48",
             "u12", "l15.5", "d12", "l31.5", "u48",
             "r32", "u24", "r15.5",
             "d24", "r16", "u24", "r32", "d40.1",
             "s"]))

    def shoot_fireball(self):
        for enemy in self.enemies.sprites():
            # If our racer is still alive, we can shoot a fireball
            if type(enemy) == Enemy.Racer:
                direction = enemy.direction
                i = random.randrange(0, 2)
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
                speed = random.randrange(3, 7)
                duration = random.randrange(1, 5) * 100
                self.enemies.add(Fireball.Fireball(speed, direction, [enemy.x,
                                                   enemy.y], duration,
                                                   (self.checkpoint + 1) *
                                                   self.fireball_strength))

    def update(self, interval):
        super(Level_4, self).update(interval)
        if self.player.x >= 111:
            Constants.STATE.set_level(1)
        # Shoot fireballs

        self.time_between_fireballs += 1
        if (self.time_between_fireballs >= Level_4.fireball_frequency):
            self.time_between_fireballs = 0
            self.shoot_fireball()
            #if self.player.y <= 0.5:
            #   Constants.STATE.set_level(2)

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
        if (damage == 0 and type(enemy) is Enemy.Boss_1):
            enemy.hurt(3)
            #Sets the game to game over if we kill the boss
            if enemy.get_health() == 0:
                self.game_over()
        #If we hit an enemy, make the enemy stop
        elif type(enemy) is Enemy.Enemy:
            enemy.stop()
        elif type(enemy) is Fireball.Fireball:
            enemy.kill()
        elif type(enemy) is Checkpoint.Checkpoint:
            #First, we check the number of the checkpoint
            checkpoint_number = enemy.number
            if checkpoint_number == self.checkpoint + 1:
                #In each of these, we gotta tell the racer it's only gonna
                # continue getting harder
                self.checkpoint = checkpoint_number
                if checkpoint_number == 1:
                    if not self.has_gotten_checkpoint_1:
                        self.beat_checkpoint_1()
                elif checkpoint_number == 2:
                    if not self.has_gotten_checkpoint_2:
                        self.beat_checkpoint_2()
                elif checkpoint_number == 3:
                    if not self.has_gotten_checkpoint_3:
                        self.beat_checkpoint_3()
                else:
                    #Here, we say congrats! You won the race (although we're
                    # going to need to do logic to determine if your'e too slow
                    self.check_finish_time()
            elif self.checkpoint < checkpoint_number:
                #TODO : Display a label like "You're going the wrong way!"
                print "Cheater!"

    def beat_checkpoint_1(self):
        self.has_gotten_checkpoint_1 = True
        # Print out some assholish label like 'You'll never catch me'
        #Increase enemy's speed
        for enemy in self.enemies.sprites():
            if type(enemy) == Enemy.Racer:
                enemy.speed += 1
                self.fireball_strength += 2
                #print "speed: " + str(enemy.speed) + ", strength: " + \
                #      str(self.fireball_strength) + ", frequency: " + \
                #      str(self.fireball_frequency)

    def beat_checkpoint_2(self):
        self.has_gotten_checkpoint_2 = True
        # Increase enemy speed and strength & frequency of fireballs
        for enemy in self.enemies.sprites():
            if type(enemy) == Enemy.Racer:
                enemy.speed += 2
                self.fireball_strength *= 2
                self.fireball_frequency *= 0.75
                #print "speed: " + str(enemy.speed) + ", strength: " + \
                #      str(self.fireball_strength) + ", frequency: " + \
                #      str(self.fireball_frequency)

    def beat_checkpoint_3(self):
        self.has_gotten_checkpoint_3 = True
        for enemy in self.enemies.sprites():
            if type(enemy) == Enemy.Racer:
                enemy.speed += 2
                self.fireball_strength *= 2
                self.fireball_frequency *= 0.5
                # print "speed: " + str(enemy.speed) + ", strength: " + \
                #      str(self.fireball_strength) + ", frequency: " + \
                #      str(self.fireball_frequency)

    def check_finish_time(self):
        for enemy in self.enemies.sprites():
            if type(enemy) == Enemy.Racer:
                enemy.timer_on = False
                if enemy.timer == 0:
                    # TODO : Handle the logic here
                    print "Super win: " + str(enemy.timer)
                elif enemy.timer <= 750:
                    # TODO : Handle the logic here (enough to beat levle,
                    # but not dominate life)
                    print "Kinda win: " + str(enemy.timer)
                else:
                    # TODO : Handle the logic here
                    "Congrats you lose, loser: " + str(enemy.timer)

import pygame
import pygame.display as display
import random
import pickle
import states.State as State
import sprites.Label as Label
import sprites.Player as Player
import sprites.Enemy as Enemy
import sprites.Speedometer as Speedometer
import map.Map as Map
import NewHigh
import GameEnded
import Menu
import sprites.EZPass as EZPass
import sprites.TollBooth as TollBooth
from Constants import Constants
from map import Map


#This is the state for playing the game
class Play(State.State):
    health = Constants.PLAYER_STARTING_HEALTH
    time = 0
    tiles = None
    START_SCORE = None
    SCORE_TIME = 0
    END_SCORE = 0

    #Code to initialize a new game instance
    def __init__(self):
        super(Play, self).__init__()
        global players, labels, background, map, key, score_label,\
            enemies, ez_passes, speedometer
        self.START_SCORE = 1000
        self.SCORE_TIME = 0
        self.is_beatable = False
        #Create global map for players to use
        global map
        map = Map.Map()
        players = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        Play.tiles = pygame.sprite.Group()
        key = pygame.sprite.Group()
        score_label = pygame.sprite.Group()
        ez_passes = pygame.sprite.Group()
        speedometer = pygame.sprite.Group()
        hp = pygame.sprite.Group()

        background = pygame.Surface(Constants.SCREEN.get_size())
        Constants.SCREEN.fill((0, 0, 0))
        labels = pygame.sprite.Group()
        h_label = Label.Label("health", "Health: 100%", (10, 10))
        s_label = Label.Label("score", "Score: ", (10, 34))
        labels.add(h_label)
        labels.add(s_label)
        map = Map.Map()
        enemy = Enemy.Enemy([39, 3.1], [
            Constants.WIDTH, Constants.HEIGHT], map, 5, "down",
            ["d4", "r2.9", "u4", "l2.9"])
        enemy2 = Enemy.Enemy([40.4, 17.5], [Constants.WIDTH, Constants.HEIGHT],
                             map, 5, "down", ["d12.5", "l16", "u12.5", "r16"])
        enemies.add(enemy)
        enemies.add(enemy2)
        ez_pass = EZPass.EZPass("ezpass", 38, 19)
        ez_passes.add(ez_pass)
        player1 = Player.Player([6, 6], [
            Constants.WIDTH, Constants.HEIGHT], map, enemies, ez_passes)
        players.add(player1)
        speedometer.add(Speedometer.Speedometer())

        self.time = 0.00

    #Function to draw the sprite groups
    def draw(self):
        #Clear the sprite groups from the screen
        players.clear(Constants.SCREEN, background)
        enemies.clear(Constants.SCREEN, background)
        Play.tiles.clear(Constants.SCREEN, background)
        # enemies.clear(Constants.SCREEN, background)
        labels.clear(Constants.SCREEN, background)
        score_label.clear(Constants.SCREEN, background)
        ez_passes.clear(Constants.SCREEN, background)
        speedometer.clear(Constants.SCREEN, background)
        # walls.clear(Constants.SCREEN, background)

        if self.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            labels.draw(Constants.SCREEN)
            display.update()
            game_over(self, True)

        else:
            # enemies.draw(Constants.SCREEN)
            #self.set_tiles()
            Play.tiles.draw(Constants.SCREEN)
            labels.draw(Constants.SCREEN)
            score_label.draw(Constants.SCREEN)
            key.draw(Constants.SCREEN)
            players.draw(Constants.SCREEN)
            enemies.draw(Constants.SCREEN)
            ez_passes.draw(Constants.SCREEN)
            speedometer.draw(Constants.SCREEN)
            # walls.draw(Constants.SCREEN)
            display.update()

    def set_tiles(self):
        for player in players.sprites():
            Play.tiles = map.render(player.x, player.y)
            player.rect.topleft = map.get_topleft(player.x, player.y)
        for enemy in enemies.sprites():
            enemy.rect.topleft = map.get_topleft(enemy.x, enemy.y)
        for ez_pass in ez_passes.sprites():
            ez_pass.rect.topleft = map.get_topleft(ez_pass.x, ez_pass.y)

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_over(self, False)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        #1 point per 1/Constants.INTERVAL cycles
        self.time += time

        self.set_tiles()
        #Update the player
        for player in players:
            player.update(Constants.INTERVAL)
            #Check if player has EZPass, if so, open the TollBooth
            if not self.is_beatable:
                if "ezpass" in player.inventory:
                    #TODO
                    #Very hackish way to do this; the score should be
                    #  on the player, so when we collect collectables
                    #  or collide, we can easily update the score.
                    # But we have more pressing things to do now.
                    self.START_SCORE += 50
                    self.is_beatable = True
                    for openable in map.openables:
                        if openable.__str__() == "t":
                            openable.open()

            if player.has_beaten_level(0):
                    game_over(self, False)
            self.health = player.calculate_health()

        for label in labels.sprites():
            if label.name == "health":
                label.update(self.health)
            elif label.name == "score":
                self.END_SCORE = self.START_SCORE - (self.time * 10)
                if self.END_SCORE <= 0:
                    game_over(self, True)
                label.update(self.END_SCORE)
        for s in score_label.sprites():
            delta = self.time - self.SCORE_TIME
            if delta > 1.2:
                score_label.remove(s)
            else:
                s.set_score_pos((126, 38 - (delta * 4)))

        for enemy in enemies:
            enemy.update(Constants.INTERVAL)

        for speed in speedometer:
            speed.update(0)


# Function to determine if the current score was a high score
def is_new_high_score(self):
    is_high = False
    f = open(Constants.HIGH_SCORE_FILE, "rb")
    try:
        scores = pickle.load(f)
    except:
        scores = []
    f.close()
    if len(scores) < 10:
        return True
    else:
        min_high_score = min(b for (a, b) in scores)
        if self.time > min_high_score:
            return True
    return False


# Define function to allow a user to restart if their health reaches 0%
def game_over(self, died):
    if died:
        Constants.STATE = GameEnded.GameEnded("GAME OVER")
    elif is_new_high_score(self):
        Constants.STATE = NewHigh.NewHigh(self.END_SCORE)
    else:
        Constants.STATE = GameEnded.GameEnded("LEVEL CLEARED")

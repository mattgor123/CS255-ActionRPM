import pygame
import pygame.display as display
import random
import pickle
import states.State as State
import sprites.Label as Label
import sprites.Player as Player
import sprites.Enemy as Enemy
import sprites.Key as Key
import sprites.Garage as Garage
import map.Map as Map
import NewHigh
import GameEnded
import Menu
from Constants import Constants
from map import Map


#This is the state for playing the game
class Play(State.State):
    health = Constants.PLAYER_STARTING_HEALTH
    time = 0
    tiles = None
    NUM_KEYS = 0
    KEY_LOC = None
    GAR_LOC = None
    START_SCORE = None
    SCORE_TIME = 0
    END_SCORE = 0

    #Code to initialize a new game instance
    def __init__(self):
        super(Play, self).__init__()
        global players, labels, background, map, key, garage, score_label,\
            enemies
        self.NUM_KEYS = 3
        self.KEY_LOC = [(15, 6), (20, 30), (30, 17)]
        self.GAR_LOC = (42, 4)
        self.START_SCORE = 1000
        self.SCORE_TIME = 0

        # read map file
        map = Map.Map()
        players = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        Play.tiles = pygame.sprite.Group()
        key = pygame.sprite.Group()
        score_label = pygame.sprite.Group()
        garage = pygame.sprite.Group()

        background = pygame.Surface(Constants.SCREEN.get_size())
        Constants.SCREEN.fill((0, 0, 0))
        labels = pygame.sprite.Group()
        h_label = Label.Label("health", "Health: 100%", (10, 10))
        s_label = Label.Label("score", "Score: ", (10, 34))
        labels.add(h_label)
        labels.add(s_label)
        map = Map.Map()
        enemy = Enemy.Enemy([39, 3.1], [
            Constants.WIDTH, Constants.HEIGHT], 2, "down")
        enemies.add(enemy)
        player1 = Player.Player([6, 6], [
            Constants.WIDTH, Constants.HEIGHT], map, enemy)
        players.add(player1)
        for i in range(self.NUM_KEYS):
            k_tl = map.get_topleft(self.KEY_LOC[i][0], self.KEY_LOC[i][1])
            key.add(Key.Key(k_tl))
        g_tl = map.get_topleft(self.GAR_LOC[0], self.GAR_LOC[1])
        garage.add(Garage.Garage(g_tl))

        self.time = 0.00

    #Function to draw the sprite groups
    def draw(self):
        #Clear the sprite groups from the screen
        players.clear(Constants.SCREEN, background)
        enemies.clear(Constants.SCREEN, background)
        Play.tiles.clear(Constants.SCREEN, background)
        # enemies.clear(Constants.SCREEN, background)
        labels.clear(Constants.SCREEN, background)
        key.clear(Constants.SCREEN, background)
        garage.clear(Constants.SCREEN, background)
        score_label.clear(Constants.SCREEN, background)
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
            g_tl = map.get_topleft(self.GAR_LOC[0], self.GAR_LOC[1])
            ind = 0
            for k in key:
                k_tl = map.get_topleft(
                    self.KEY_LOC[ind][0], self.KEY_LOC[ind][1])
                k.update(k_tl)
                ind += 1
            garage.update(g_tl)
            key.draw(Constants.SCREEN)
            garage.draw(Constants.SCREEN)
            players.draw(Constants.SCREEN)
            enemies.draw(Constants.SCREEN)
            # walls.draw(Constants.SCREEN)
            display.update()

    #Only specific key event we will handle for now is 'q' or 'r' to restart

    def set_tiles(self):
        for player in players.sprites():
            Play.tiles = map.render(player.x, player.y)
            player.rect.topleft = map.get_topleft(player.x, player.y)
        for enemy in enemies.sprites():
            enemy.rect.topleft = map.get_topleft(enemy.x, enemy.y)

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
            if player.update(Constants.INTERVAL):
                if len(score_label) != 0:
                    for s in score_label:
                        score_label.remove(s)
                sl = Label.Label("sl", "-20", (126, 38))
                sl.set_green(False)
                self.START_SCORE -= 1
                self.SCORE_TIME = self.time
                score_label.add(sl)
            k = player.check_key(key)
            if k is not None:
                key.remove(k[0])
                self.KEY_LOC.remove(self.KEY_LOC[k[1]])
                self.START_SCORE += 200
                if len(score_label) != 0:
                    for s in score_label:
                        score_label.remove(s)
                sl = Label.Label("sl", "+200", (126, 38))
                self.SCORE_TIME = self.time
                score_label.add(sl)
                self.NUM_KEYS -= 1
                if self.NUM_KEYS is 0:
                    for g in garage:
                        g.open_door()
            if player.check_garage(garage):
                labels.draw(Constants.SCREEN)
                display.update()
                game_over(self, False)

        #Determine current health status & update Label
        for player in players.sprites():
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

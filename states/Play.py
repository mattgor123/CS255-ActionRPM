import pygame
import pygame.display as display
import random
import pickle
import states.State as State
import sprites.Label as Label
import sprites.Player as Player
import sprites.Enemy as Enemy
import map.Map as Map
import NewHigh
import GameEnded
import Menu
from Constants import Constants


#This is the state for playing the game
class Play(State.State):
    health = Constants.PLAYER_STARTING_HEALTH
    time = 0

    #Code to initialize a new game instance
    def __init__(self):
        super(Play, self).__init__()
        global players, labels, background, maps, player, map

        # read map file
        map = Map.Map()
        players = pygame.sprite.Group()
        player = Player.Player(map.get_top_left(40, 30), [
            Constants.WIDTH, Constants.HEIGHT], Constants.DIFFICULTY)
        players.add(player)
        maps = map.render(player.p_x, player.p_y)
        maps.update()

        background = pygame.Surface(Constants.SCREEN.get_size())
        Constants.SCREEN.fill((0, 0, 0))
        labels = pygame.sprite.Group()
        h_label = Label.Label("health", "Health: 100%", (10, 10))
        s_label = Label.Label("score", "Score: ", (10, 34))
        labels.add(h_label)
        labels.add(s_label)
        self.time = 0.00

    #Function to draw the sprite groups
    def draw(self):
        #Clear the sprite groups from the screen
        maps = map.render(player.p_x, player.p_y)
        players.clear(Constants.SCREEN, background)
        labels.clear(Constants.SCREEN, background)
        maps.clear(Constants.SCREEN, background)

        if self.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            labels.draw(Constants.SCREEN)
            display.update()
            game_over(self)

        else:
            maps.update()
            maps.draw(Constants.SCREEN)
            labels.draw(Constants.SCREEN)
            players.draw(Constants.SCREEN)
            display.update()

    #Only specific key event we will handle for now is 'q' or 'r' to restart
    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_over(self)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        #1 point per 1/Constants.INTERVAL cycles
        self.time += time

        #Update the player
        players.update(Constants.INTERVAL)
        for player in players.sprites():
                dir_changed = player.dir_changed
                direction = player.direction

        #Determine current health status & update Label
        for player in players.sprites():
            self.health = player.calculate_health()
        for label in labels.sprites():
            if label.name == "health":
                label.update(self.health)
            elif label.name == "score":
                label.update(self.time)


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
def game_over(self):
    if is_new_high_score(self):
        Constants.STATE = NewHigh.NewHigh(self.time)
    else:
        Constants.STATE = GameEnded.GameEnded()

# ActionRPM
# VGD (600.255)
# Assignment 2
# 9/21/2014

import pygame
import pygame.display as display
import pygame.event as event
import pygame.time as time
import random

# Import our Label, Player and Enemy Sprite Classes
import Label
import Player
import Enemy
import State



# Constants (ALL MUST BE INTEGERS except INTERVAL)
class Globals():
    WIDTH = None
    HEIGHT = None
    PLAYER_SPEED = 500
    ENEMY_COUNT = 13
    ENEMY_SPEEDS = 6
    DIFFICULTY = 10  # 1-10
    INTERVAL = .01
    SCREEN = None
    STATE = None

class Game(State.State):
    def __init__(self):
        global players, enemies, labels, background
        # Label sprite stuff
        labels = pygame.sprite.Group()
        h_label = Label.Label("health", "Health: 100%", (0, 0))
        fps_label = Label.Label("fps", "Frames/Second: ", (0, 24))
        spf_label = Label.Label("spf", "Seconds/Frame: ", (0, 48))
        upf_label = Label.Label("upf", "Updates/Frame: ", (0, 72))
        labels.add(h_label)
        labels.add(fps_label)
        labels.add(spf_label)
        labels.add(upf_label)

        # Player sprite stuff
        players = pygame.sprite.Group()
        player1 = Player.Player([Globals.WIDTH / 2, Globals.HEIGHT / 2], [Globals.WIDTH, Globals.HEIGHT],
                                Globals.PLAYER_SPEED, Globals.DIFFICULTY)
        players.add(player1)

        # Enemy sprite stuff
        enemies = pygame.sprite.Group()
        for i in range(Globals.ENEMY_COUNT):
            enemy_speed = random.randint(1, Globals.ENEMY_SPEEDS) * Globals.PLAYER_SPEED * 2 / \
                          Globals.ENEMY_SPEEDS
            new_enemy = Enemy.Enemy([random.randint(0, Globals.WIDTH - player1.rect.width),
                                    random.randint(0, Globals.HEIGHT -
                                    player1.rect.height)], [Globals.WIDTH, Globals.HEIGHT],
                                    enemy_speed, direction=random.randint(1, 8))
            enemies.add(new_enemy)
        pass
    def draw(self, screen):
        pass
    def keyEvent(self, event):
        pass
    def update(self, time):
        pass


# Define function to initialize game state so you can restart
def init():
    # Initialize Screen
    pygame.init()
    Globals.WIDTH = 800
    Globals.HEIGHT = 600
    Globals.SCREEN = display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    Game.background = pygame.Surface(Globals.SCREEN.get_size())


    Globals.STATE = Game()


# Define function to allow a user to restart if their health reaches 0%
def game_over():
    global myFont
    for label1 in labels:
        myFont = label1.font
    game_over_surface = myFont.render(
        'Game Over - Would you like to restart? (Y/N)', 1, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = Globals.SCREEN.get_rect().center
    Globals.SCREEN.blit(game_over_surface, game_over_rect)
    display.update()
    while True:
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_y:
                    Globals.SCREEN.fill((0, 0, 0))
                    init()
                    return
                if eve.key == pygame.K_n or eve.key == pygame.K_ESCAPE:
                    exit()


#Define function to actually perform the game logic (update positions,
# health, etc.)
def main_loop():
    #Clock code adapted from Peter's leftover-interval.py
    global direction, dir_changed
    clock = time.Clock()
    current_time = time.get_ticks()
    leftover = 0.0

    while True:
        #Clear the sprite groups (more efficient than filling fully)
        players.clear(Globals.SCREEN, Game.background)
        enemies.clear(Globals.SCREEN, Game.background)
        labels.clear(Globals.SCREEN, Game.background)

        #Set up clock stuff
        new_time = time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        clock.tick()

        #Update the Player & Enemy
        updates = 0
        leftover += frame_time

        while leftover > Globals.INTERVAL:
            players.update(Globals.INTERVAL)
            for player in players.sprites():
                dir_changed = player.dir_changed
                direction = player.direction
            enemies.update(dir_changed, direction, Globals.INTERVAL)
            leftover -= Globals.INTERVAL
            updates += 1

        #Determine current health status & update Label
        for player in players.sprites():
            health = player.calculate_health()
        dead = (health <= 0)

        #Update the labels
        for label in labels.sprites():
            if label.name == "health":
                label.update(health)
            elif label.name == "fps":
                label.update(clock.get_fps())
            elif label.name == "spf":
                label.update(frame_time)
            elif label.name == "upf":
                label.update(updates)

        if dead:
            #We just want to see health 0% and prompt the game over message
            labels.draw(screen)
            display.update()
            game_over()

        else:
            #we want the Label always on top, with Player on top of enemies
            enemies.draw(Globals.SCREEN)
            players.draw(Globals.SCREEN)
            labels.draw(Globals.SCREEN)
            display.update()

        #Begin key presses
        pygame.event.pump()
        for eve in event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN and eve.key == pygame.K_ESCAPE:
                exit()

# Run the game!
def main():
    init()
    main_loop()

if __name__ == "__main__":
    main();

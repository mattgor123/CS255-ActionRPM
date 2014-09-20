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

# Constants (ALL MUST BE INTEGERS except INTERVAL)
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 500
ENEMY_COUNT = 13
ENEMY_SPEEDS = 6
DIFFICULTY = 10  # 1-10
INTERVAL = .01

# Initialize Screen
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size())


# Define function to initialize game state so you can restart
def init():
    global players, enemies, labels

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
    player1 = Player.Player([WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT],
                            PLAYER_SPEED, DIFFICULTY)
    players.add(player1)

    # Enemy sprite stuff
    enemies = pygame.sprite.Group()
    for i in range(ENEMY_COUNT):
        enemy_speed = random.randint(1, ENEMY_SPEEDS) * PLAYER_SPEED * 2 / \
                      ENEMY_SPEEDS
        new_enemy = Enemy.Enemy([random.randint(0, WIDTH - player1.rect.width),
                                random.randint(0, HEIGHT -
                                player1.rect.height)], [WIDTH, HEIGHT],
                                enemy_speed, direction=random.randint(1, 8))
        enemies.add(new_enemy)


# Define function to allow a user to restart if their health reaches 0%
def game_over():
    global myFont
    for label1 in labels:
        myFont = label1.font
    game_over_surface = myFont.render(
        'Game Over - Would you like to restart? (Y/N)', 1, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = screen.get_rect().center
    screen.blit(game_over_surface, game_over_rect)
    display.update()
    while True:
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_y:
                    screen.fill((0, 0, 0))
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
        players.clear(screen, background)
        enemies.clear(screen, background)
        labels.clear(screen, background)

        #Set up clock stuff
        new_time = time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        clock.tick()

        #Update the Player & Enemy
        updates = 0
        leftover += frame_time

        while leftover > INTERVAL:
            players.update(INTERVAL)
            for player in players.sprites():
                dir_changed = player.dir_changed
                direction = player.direction
            enemies.update(dir_changed, direction, INTERVAL)
            leftover -= INTERVAL
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
            enemies.draw(screen)
            players.draw(screen)
            labels.draw(screen)
            display.update()

        #Begin key presses
        pygame.event.pump()
        for eve in event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN and eve.key == pygame.K_ESCAPE:
                exit()

# Run the game!
init()
main_loop()

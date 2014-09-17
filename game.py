# ActionRPM
# VGD (600.255)
# Assignment 2
# 9/21/2014

import pygame as game
import pygame.display as display
import pygame.event as event
import pygame.time as time
import random

# Import our Player and Enemy Classes
import player
import enemy

# Constants
WIDTH = 800
HEIGHT = 600
PLAYERSPEED = 1
ENEMYCOUNT = 13
ENEMYSPEEDS = 3

# Initialize Screen
game.init()
screen = display.set_mode( (WIDTH, HEIGHT) )
WIDTH, HEIGHT = screen.get_size()

# Initialize Clock
clock = time.Clock()
current_time = time.get_ticks()
leftover = 0.0
updates = 0

# Player sprite stuff
player1 = player.player( [0, 0] , [WIDTH, HEIGHT],  PLAYERSPEED )

# Enemy sprite stuff
enemies = game.sprite.Group()
for i in range(ENEMYCOUNT):
    newenemy = enemy.enemy( [random.randint(0,WIDTH-50), random.randint(0,HEIGHT-25)], [WIDTH, HEIGHT],
                            speed=random.randint(1,ENEMYSPEEDS), direction = random.randint(1,8))
    enemies.add(newenemy)

while True:
    new_time = time.get_ticks()
    frame_time = (new_time - current_time) / 1000.0
    current_time = new_time

    clock.tick()

    screen.fill( (0, 0, 0) )

    screen.blit(player1.image, player1.rect)
    enemies.draw(screen)
    # draw stuff

    display.update()

    updates = 0
    leftover += frame_time
    while leftover > 0.01:
        # draw stuff
        leftover -= 0.01
        updates += 1

#Begin key presses
    game.event.pump()

    for eve in event.get():
        if eve.type == game.QUIT:
            exit()
        elif eve.type == game.KEYDOWN and eve.key == game.K_ESCAPE:
            exit()

    player1.update()
    enemies.update(player1.dirchanged, player1.direction)
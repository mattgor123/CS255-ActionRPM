# ActionRPM
# VGD (600.255)
# Assignment 2
# 9/21/2014

import pygame as game
import pygame.display as display
import pygame.event as event
import pygame.time as time

# Import our Player and Enemy Classes
import Player
import Enemy

# Constants
WIDTH = 800
HEIGHT = 600
RADIUS = 100
SPEED = 4 * 60 

# Initialize Screen
game.init()
screen = display.set_mode( (WIDTH, HEIGHT) )
WIDTH, HEIGHT = screen.get_size()

# Initialize Clock
clock = time.Clock()
current_time = time.get_ticks()
leftover = 0.0
updates = 0

while True:
    new_time = time.get_ticks()
    frame_time = (new_time - current_time) / 1000.0
    current_time = new_time

    clock.tick()

    screen.fill( (0, 0, 0) )

    # draw stuff

    display.flip()

    updates = 0
    leftover += frame_time
    while leftover > 0.01:
        # draw stuff
        leftover -= 0.01
        updates += 1

    for eve in event.get():
        if eve.type == game.QUIT:
            exit()
        elif eve.type == game.KEYDOWN and eve.key == game.K_ESCAPE:
            exit()
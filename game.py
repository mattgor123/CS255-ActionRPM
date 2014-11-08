# ActionRPM
# VGD (600.255)
# Assignment 2
# 9/21/2014

import pygame
import pygame.display as display
import pygame.event as event
import pygame.time as time

# Import our State and Constants classes
from states.Constants import Constants
import states.Title as Title
import states.Menu as Menu

# Define function to actually perform the game logic (update positions,
# health, etc.)


def main_loop():

    # Clock code adapted from Peter's leftover-interval.py
    clock = time.Clock()
    current_time = time.get_ticks()
    leftover = 0.0

    while True:
        Constants.STATE.draw()
        #Set up clock stuff
        new_time = time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        clock.tick()

        #Update the Player & Enemy
        updates = 0
        leftover += frame_time

        while leftover > Constants.INTERVAL:
            Constants.STATE.update(Constants.INTERVAL)
            leftover -= Constants.INTERVAL
            updates += 1
            #if Constants.STATE == Play.Play:
            #    params = [clock.get_fps(),frame_time,updates]
            #    Constants.STATE.update_labels(params)

        #Begin key presses
        pygame.event.pump()
        for eve in event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN and eve.key == pygame.K_m and \
                    eve.mod & (pygame.KMOD_CTRL or pygame.KMOD_LCTRL):
                Constants.STATE = Menu.Menu()
            else:
                Constants.STATE.keyEvent(eve)


# Define function to initialize game state so you can restart
def init():
    # Initialize Screen
    pygame.init()
    pygame.display.set_caption("ActionRPM")
    # Create the high scores file
    try:
        f = open(Constants.HIGH_SCORE_FILE, 'rb')
        f.close()
    except:
        f = open(Constants.HIGH_SCORE_FILE, 'wb')
        f.close()
    # Set the constants
    Constants.WIDTH = 800
    Constants.HEIGHT = 600
    Constants.SCREEN = display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    # Display the title screen
    Constants.STATE = Title.Title()
    Constants.STATE.__init__()

init()
main_loop()

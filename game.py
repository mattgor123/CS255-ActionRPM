"""Game.py is the main module that runs the actionRPM game"""

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
    """Main loop for running the actionRPM game"""
    # Clock code adapted from Peter's leftover-interval.py
    clock = time.Clock()
    current_time = time.get_ticks()
    leftover = 0.0

    while True:
        Constants.STATE.draw()
        # Set up clock stuff
        new_time = time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        clock.tick()

        #Update the Player & Enemy
        leftover += frame_time

        while leftover > Constants.INTERVAL:
            Constants.STATE.update(Constants.INTERVAL)
            leftover -= Constants.INTERVAL

        #Begin key presses
        pygame.event.pump()
        for eve in event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN and eve.key == pygame.K_m and \
                            eve.mod & (pygame.KMOD_CTRL or pygame.KMOD_LCTRL):
                Constants.STATE = Menu.Menu()
                #elif eve.type == pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pos())
            else:
                Constants.STATE.keyEvent(eve)


# Define function to initialize game state so you can restart
def init():
    """Init all of the variables needed for the main driver of ActionRPM"""
    pygame.init()
    pygame.display.set_caption("ActionRPM")
    # Create the high scores file
    try:
        file_high_score = open(Constants.HIGH_SCORE_FILE, 'rb')
        file_high_score.close()
    except IOError:
        file_high_score = open(Constants.HIGH_SCORE_FILE, 'wb')
        file_high_score.close()
    # Set the constants
    Constants.WIDTH = 800
    Constants.HEIGHT = 600
    Constants.SCREEN = display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    # Display the title screen
    Constants.STATE = Title.Title()
    Constants.STATE.__init__()


init()
main_loop()

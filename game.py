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

# Constants (ALL MUST BE INTEGERS)
WIDTH = 800
HEIGHT = 600
PLAYERSPEED = 1
ENEMYCOUNT = 13
ENEMYSPEEDS = 3

# Initialize Screen
game.init()
screen = display.set_mode( (WIDTH, HEIGHT) )
# Damage label font (will make it sexier later)
myfont = game.font.Font(None,30)

#Define function to initialize game state so you can restart
def init():
    global player1, enemies

    # Player sprite stuff
    player1 = player.player( [0, 0] , [WIDTH, HEIGHT],  PLAYERSPEED )

    # Enemy sprite stuff
    enemies = game.sprite.Group()
    for i in range(ENEMYCOUNT):
        newenemy = enemy.enemy( [random.randint(0,WIDTH-player1.rect.width), random.randint(0,HEIGHT-player1.rect.height)],
                                [WIDTH, HEIGHT],speed=random.randint(1,ENEMYSPEEDS), direction = random.randint(1,8))
        enemies.add(newenemy)

#Define function to allow a user to restart if their health reaches 0%
def game_over():
    gameOverSurface = myfont.render('Game Over - Would you like to restart? (Y/N)',1,(255,255,255))
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.center = screen.get_rect().center
    screen.blit(gameOverSurface,gameOverRect)
    display.update()
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            elif event.type == game.KEYDOWN:
                if event.key == game.K_y:
                    init()
                    return
                if event.key == game.K_n or event.key == game.K_ESCAPE:
                    exit()

#Define function to actually perform the game logic (update positions, health, etc.)
def main_loop():
    while True:

        #Determine current health status
        health = player1.calchealth()
        dead = (health <= 0)

        #Get appropriate label color based on health
        if (health < 25):
            COLOR = (255,0,0)
        elif (health < 75):
            COLOR = (255,255,0)
        else:
            COLOR = (0,255,0)

        label = myfont.render("Health: " + str(health) + "%",1,COLOR)

        #redraw stuff
        screen.fill( (0, 0, 0) )
        screen.blit(player1.image, player1.rect)
        enemies.draw(screen)
        screen.blit(label,(0,0))
        display.update()

        if dead:
            game_over()

        #Begin key presses
        game.event.pump()
        for eve in event.get():
            if eve.type == game.QUIT:
                exit()
            elif eve.type == game.KEYDOWN and eve.key == game.K_ESCAPE:
                exit()

        player1.update()
        enemies.update(player1.dirchanged, player1.direction)

init()
main_loop()
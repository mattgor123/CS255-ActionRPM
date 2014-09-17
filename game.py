# ActionRPM
# VGD (600.255)
# Assignment 2
# 9/21/2014

import pygame as game
import pygame.display as display
import pygame.event as event
import pygame.time as time
import label
import random

# Import our Player and Enemy Classes
import player
import enemy

# Constants (ALL MUST BE INTEGERS)
WIDTH = 800
HEIGHT = 600
PLAYERSPEED = 500
ENEMYCOUNT = 13
ENEMYSPEEDS = 6
DIFFICULTY = 10 #1-10
INTERVAL = .01

# Initialize Screen
game.init()
screen = display.set_mode( (WIDTH, HEIGHT) )
background = game.Surface(screen.get_size())


#Define function to initialize game state so you can restart
def init():
    global players, enemies, labels

    #Label sprite stuff
    labels = game.sprite.Group()
    hlabel = label.label("health","Health: 100%", (0,0))
    fpslabel = label.label("fps","Seconds/Frame: " ,(0,24))
    spflabel = label.label("spf","Frames/Second: " , (0,48))
    upflabel = label.label("upf","Updates/Frame: ", (0,72))
    labels.add(hlabel)
    labels.add(fpslabel)
    labels.add(spflabel)
    labels.add(upflabel)

    # Player sprite stuff
    players = game.sprite.Group()
    player1 = player.player( [WIDTH/2, HEIGHT/2] , [WIDTH, HEIGHT],  PLAYERSPEED, DIFFICULTY )
    players.add(player1)

    # Enemy sprite stuff
    enemies = game.sprite.Group()
    for i in range(ENEMYCOUNT):
        newenemy = enemy.enemy( [random.randint(0,WIDTH-player1.rect.width), random.randint(0,HEIGHT-player1.rect.height)],
                                [WIDTH, HEIGHT],speed=random.randint(1,ENEMYSPEEDS)*PLAYERSPEED/2,
                                direction = random.randint(1,8))
        enemies.add(newenemy)

#Define function to allow a user to restart if their health reaches 0%
def game_over():
    for label in labels:
        myfont = label.font
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
                    screen.fill((0,0,0))
                    init()
                    return
                if event.key == game.K_n or event.key == game.K_ESCAPE:
                    exit()

#Define function to actually perform the game logic (update positions, health, etc.)
def main_loop():
    #Clock code adapted from Peter's leftover-interval.py
    clock = time.Clock()
    current_time = time.get_ticks()
    leftover = 0.0
    updates = 0

    while True:
        #Clear the sprite groups (more efficient than filling fully)
        players.clear(screen,background)
        enemies.clear(screen,background)
        labels.clear(screen,background)

        #Set up clock stuff
        new_time = time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        clock.tick()

        #Update the player & enemy
        updates = 0
        leftover += frame_time

        while leftover > INTERVAL:
            players.update(INTERVAL)
            for player in players.sprites():
                dirchanged = player.dirchanged
                direction = player.direction
            enemies.update(dirchanged, direction, INTERVAL)
            leftover -= INTERVAL
            updates += 1

        #Determine current health status & update label
        for player in players.sprites():
            health = player.calchealth()
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

        #we want the label always on top, with player on top of enemies
        enemies.draw(screen)
        players.draw(screen)
        labels.draw(screen)
        display.update()

        #Begin key presses
        game.event.pump()
        for eve in event.get():
            if eve.type == game.QUIT:
                exit()
            elif eve.type == game.KEYDOWN and eve.key == game.K_ESCAPE:
                exit()

init()
main_loop()

import pygame as game
from math import fabs
import pygame
import util.SpriteSheet as SP
import sprites.Label as Label
import states.Constants as Constants


class Enemy(game.sprite.Sprite):
    image = None
    screen_width = 0
    screen_height = 0
    should_change_motion_direction = False
    FRAME_SLOW = 10
    # Number of cycles the enemy will stop for after hitting an enemy
    max_stop_time = 100

    # Enemy constructor takes an initial location, screendims for collisions,
    # a speed, and a starting direction
    def __init__(self, location, screensize,
                 speed, direction, move_array):

        game.sprite.Sprite.__init__(self)

        Enemy.screen_width = screensize[0]
        Enemy.screen_height = screensize[1]
        self.frame = 0
        self.frameCalls = 0
        if Enemy.image is None:
            # make all of the appropriate transformations of the image based
            # on direction of travel

            sprites = SP.loadSheet(
                "images/sprites/enemyfullhealthlights.png", 52, 26, [3, 1])
            Enemy.right = sprites[0]
            Enemy.left = SP.rotateSprites(Enemy.right, 180)
            Enemy.up = SP.rotateSprites(Enemy.right, 90)
            Enemy.down = SP.rotateSprites(Enemy.right, -90)
            Enemy.upright = SP.rotateSprites(Enemy.right, 45)
            Enemy.upleft = SP.rotateSprites(Enemy.right, 135)
            Enemy.downright = SP.rotateSprites(Enemy.right, -45)
            Enemy.downleft = SP.rotateSprites(Enemy.right, -135)

        self.direction = direction
        self.set_direction(direction)
        self.set_image()
        #set the speed & get the rectangle

        self.speed = speed
        self.rect = self.image.get_rect()

        #make sure it is in the appropriate location
        self.rect.topleft = location
        #get the width & height of screen
        self.width = screensize[0]
        self.height = screensize[1]
        self.x = location[0]
        self.y = location[1]
        self.movements = move_array
        self.current_move = 0
        self.old_pos_x = location[0]
        self.old_pos_y = location[1]
        #This variable keeps track of the number of cycles
        #the enemy has waited before restarting
        #If 0, enemy continues as normal
        #Enemy will stay stopped until stop_time == max_stop_time
        self.stop_time = 0

    # this is the update method with a parameter - it ensures the Enemy is
    # facing opposite dir of the Player then updates
    def update(self, interval, player_coordinates):
        self.move(interval)

    def get_strength(self):
        return 3

    #this moves the Enemy to where he is supposed to be based on the direction
    '''
    Note : We wrote this function interpreting 'look' to mean the direction
    in which the Enemy is facing.
    Please have pity on our souls for the duplicated/relatively ugly
    code...not currently being used.
    '''

    def move(self, interval):
        #If the stop_time is max_stop_time, then the enemy waited long enough
        #and can restart moving
        #If the stop_time is 0, it indicates that the car can continue moving
        if self.stop_time == self.max_stop_time or self.stop_time == 0:
            #Make sure stop time is back at 0 once we are moving again
            self.stop_time = 0

            curr_action = self.movements[self.current_move]
            distance_moved_x = fabs(self.old_pos_x - self.x)
            distance_moved_y = fabs(self.old_pos_y - self.y)

            if (curr_action[0:1] == "d"):
                self.y += self.speed * interval
                self.direction = "down"
                self.set_direction("down")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_y > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_y = self.y

            elif (curr_action[0:1] == "r"):
                self.x += self.speed * interval
                self.direction = "right"
                self.set_direction("right")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_x > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_x = self.x

            elif (curr_action[0:1] == "u"):
                self.y -= self.speed * interval
                self.direction = "up"
                self.set_direction("up")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_y > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_y = self.y

            elif (curr_action[0:1] == "l"):
                self.direction = "left"
                self.set_direction("left")
                self.x -= self.speed * interval
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_x > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_x = self.x

        else:
            #add one to the number of cycles the enemy has waited
            self.stop_time += 1

    #method to set the direction
    def set_direction(self, direction):
        #set the image based on the direction
        if direction == "right":
            self.IMAGES = Enemy.right
        elif direction == "downright":
            self.IMAGES = Enemy.downright
        elif direction == "down":
            self.IMAGES = Enemy.down
        elif direction == "downleft":
            self.IMAGES = Enemy.downleft
        elif direction == "left":
            self.IMAGES = Enemy.left
        elif direction == "upleft":
            self.IMAGES = Enemy.upleft
        elif direction == "up":
            self.IMAGES = Enemy.up
        elif direction == "upright":
            self.IMAGES = Enemy.upright

        self.set_image()

    def set_image(self):
        if self.frame >= len(self.IMAGES):
            self.frame = 0
        self.image = self.IMAGES[self.frame]
        self.frameCalls += 1

        if self.frameCalls % Enemy.FRAME_SLOW == 0:
            self.frame += 1

    def stop(self):
        #Once stop_time is > 0, the enemy will stop
        #Enemy will continue to be stopped until
        #The cycle count reaches our max_stop_time
        #Move function takes care of restarting enemy
        self.stop_time = 1


class Boss_1(game.sprite.Sprite):
    image = None
    screen_width = 0
    screen_height = 0
    should_change_motion_direction = False
    FRAME_SLOW = 10
    # Number of cycles the enemy will stop for before moving again
    max_wait_time = 65

    # Enemy constructor takes an initial location, screendims for collisions,
    # a speed, and a starting direction
    def __init__(self, location, screensize):
        game.sprite.Sprite.__init__(self)
        Boss_1.screen_width = screensize[0]
        Boss_1.screen_height = screensize[1]
        self.frame = 0
        self.frameCalls = 0
        if Boss_1.image is None:
            # make all of the appropriate transformations of the image based
            # on direction of travel

            sprites = SP.loadSheet(
                "images/sprites/boss_1.png", 52, 26, [2, 1])
            Boss_1.right = sprites[0]
            Boss_1.left = SP.rotateSprites(Boss_1.right, 180)
            Boss_1.up = SP.rotateSprites(Boss_1.right, 90)
            Boss_1.down = SP.rotateSprites(Boss_1.right, -90)
            Boss_1.upright = SP.rotateSprites(Boss_1.right, 45)
            Boss_1.upleft = SP.rotateSprites(Boss_1.right, 135)
            Boss_1.downright = SP.rotateSprites(Boss_1.right, -45)
            Boss_1.downleft = SP.rotateSprites(Boss_1.right, -135)

        self.waiting = False
        self.direction = "right"
        self.set_direction(self.direction)
        self.set_image()
        #set the speed & get the rectangle

        self.rect = self.image.get_rect()

        #make sure it is in the appropriate location
        self.rect.topleft = location
        #get the width & height of screen
        self.width = screensize[0]
        self.height = screensize[1]
        self.x = location[0]
        self.y = location[1]
        self.current_move = 0
        self.old_pos_x = location[0]
        self.old_pos_y = location[1]
        #This variable keeps track of the number of cycles
        #the enemy has waited before restarting
        #If 0, enemy continues as normal
        #Enemy will stay stopped until stop_time == max_stop_time
        self.waited_time = 0
        self.moved_time = 0
        self.speed = 7
        self.active_distance = 15

        #Initial strength for car
        self.strength = 0

        #Set as 500 to give him a little more strength
        self.health = 500

        #Original transport variables
        self.is_transporting = False
        self.transport_time = 0
        self.transport_location = None

    # this is the update method with a parameter - it ensures the Enemy is
    # facing the directopm of the Player then moves
    def update(self, interval, player_coordinates):
        #This means our guy will stay flashed for a few seconds
        if (self.is_transporting and self.transport_time < 200):
            self.strength = 1
            #self.waiting = True
            self.frame = 1
            self.set_image()
            self.transport_time += 1
        #This means its time to transpot our dude
        elif (self.is_transporting and self.transport_time >= 200):
            #The next few blocks reset the enemy's
            self.rect.topleft = self.transport_location
            self.x = self.transport_location[0]
            self.y = self.transport_location[1]
            self.current_move = 0
            self.old_pos_x = self.transport_location[0]
            self.old_pos_y = self.transport_location[1]
            #Reset our transport variables
            self.transport_time = 0
            self.is_transporting = False
            self.transport_location = None
        #This means we are not currently doing the transport
        else:
            self.turn(interval, player_coordinates)

    def hurt(self, damage):
        if self.health - damage < 0:
            self.health = 0
        else:
            self.health -= damage
            #Must use the health out of 500
            #So 375/500 = 75
            if self.health + damage >= 375 and self.health < 375:
                #This will put the health done below 75$
                self.health = 374
                self.transport([70, 40])
            elif self.health + damage >= 250 and self.health < 250:
                #This will put the health done below 75$
                self.health = 249
                self.transport([8, 53])
            elif self.health + damage >= 125 and self.health < 125:
                #This will put the health done below 75$
                self.health = 124
                self.transport([46, 17])

    def transport(self, location):
        self.is_transporting = True
        self.transport_time = 0
        self.transport_location = location

    def get_strength(self):
        return self.strength

    #this moves the Enemy to where he is supposed to be based on the direction
    def turn(self, interval, player_coordinates):

        if self.waited_time >= 2 * Boss_1.max_wait_time:
            self.waited_time = 0
            self.speed = 5
            self.waiting = False
            self.set_direction(self.direction)

        #This means our boss has waited long enough to move
        if Boss_1.max_wait_time <= self.waited_time < 2 * Boss_1.max_wait_time:
            #If our guy is gonna move, then he should be hurting the player
            self.strength = 3
            self.waiting = False
            self.move(interval)
            self.set_direction(self.direction)
            self.waited_time += 1
        #This if statement checks if the player is within 3 blocks of the boss
        elif abs(self.x - player_coordinates[0]) <= self.active_distance and \
                abs(self.y - player_coordinates[1]) <= self.active_distance:
            self.waited_time += 1
            #Negative strength indicates that our enemy can be hurt
            self.strength = 0
            self.waiting = True
            if self.x < player_coordinates[0] and \
                    abs(self.y - player_coordinates[1]) <= 1:
                self.direction = "right"
                self.set_direction("right")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.x > player_coordinates[0] and \
                    abs(self.y - player_coordinates[1]) <= 1:
                self.direction = "left"
                self.set_direction("left")
                self.rect = self.image.get_rect(center=self.rect.center)
            if self.y < player_coordinates[1] and \
                    abs(self.x - player_coordinates[0]) <= 1:
                self.direction = "down"
                self.set_direction("down")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.y > player_coordinates[1] and \
                    abs(self.x - player_coordinates[0]) <= 1:
                self.direction = "up"
                self.set_direction("up")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.x < player_coordinates[0] and \
                    self.y - player_coordinates[1] >= 1:
                self.direction = "upright"
                self.set_direction("upright")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.x < player_coordinates[0] and \
                    self.y - player_coordinates[1] <= -1:
                self.direction = "downright"
                self.set_direction("downright")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.x > player_coordinates[0] and self.y - \
                    player_coordinates[1] >= 1:
                self.direction = "upleft"
                self.set_direction("upleft")
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.x > player_coordinates[0] and \
                    self.y - player_coordinates[1] <= -1:
                self.direction = "downleft"
                self.set_direction("downleft")
                self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, interval):

        if self.direction == "up":
            self.y -= self.speed * interval
        elif (self.direction == "down"):
            self.y += self.speed * interval
        elif (self.direction == "right"):
            self.x += self.speed * interval
        elif (self.direction == "left"):
            self.x -= self.speed * interval
        if (self.direction == "upright"):
            self.x += self.speed * interval * .7071
            self.y -= self.speed * interval * .7071
        elif (self.direction == "downright"):
            self.x += self.speed * interval * .7071
            self.y += self.speed * interval * .7071
        elif (self.direction == "upleft"):
            self.x -= self.speed * interval * .7071
            self.y -= self.speed * interval * .7071
        elif (self.direction == "downleft"):
            self.x -= self.speed * interval * .7071
            self.y += self.speed * interval * .7071

    #method to set the direction
    def set_direction(self, direction):
        #set the image based on the direction
        if direction == "right":
            self.IMAGES = Boss_1.right
        elif direction == "downright":
            self.IMAGES = Boss_1.downright
        elif direction == "down":
            self.IMAGES = Boss_1.down
        elif direction == "downleft":
            self.IMAGES = Boss_1.downleft
        elif direction == "left":
            self.IMAGES = Boss_1.left
        elif direction == "upleft":
            self.IMAGES = Boss_1.upleft
        elif direction == "up":
            self.IMAGES = Boss_1.up
        elif direction == "upright":
            self.IMAGES = Boss_1.upright

        self.set_image()

    def set_image(self):
        if not self.waiting:
            self.frame = 0

        self.image = self.IMAGES[self.frame]
        self.frameCalls += 1

        if self.frameCalls % Boss_1.FRAME_SLOW == 0:
            self.frame += 1

        if (self.frame == 1 and not self.waiting) or (self.frame == len(
                self.IMAGES) and self.waiting):
            self.frame = 0

    def get_health(self):
        """Returns the health of the enemy from 0-100"""
        #Divide by 5 to get the ratio out of 100
        return self.health / 5


class Racer(game.sprite.Sprite):
    image = None
    screen_width = 0
    screen_height = 0
    FRAME_SLOW = 10
    # Number of cycles the enemy will stop for after hitting an enemy
    max_stop_time = 100
    right = None
    up = None
    left = None
    down = None
    downleft = None
    downright = None
    upleft = None
    upright = None
    speed = None

    # Enemy constructor takes an initial location, screendims for collisions,
    # a speed, and a starting direction
    def __init__(self, location, screensize,
                 speed, direction, move_array):
        game.sprite.Sprite.__init__(self)
        Enemy.screen_width = screensize[0]
        Enemy.screen_height = screensize[1]
        if Racer.image is None:
            # make all of the appropriate transformations of the image based
            # on direction of travel

            Racer.image = game.image.load("images/sprites/racer.png")
            Racer.right = Racer.image
            Racer.left = game.transform.rotate(Racer.right, 180)
            Racer.up = game.transform.rotate(Racer.right, 90)
            Racer.down = game.transform.rotate(Racer.right, -90)
            Racer.upright = game.transform.rotate(Racer.right, 45)
            Racer.upleft = game.transform.rotate(Racer.right, 135)
            Racer.downright = game.transform.rotate(Racer.right, -45)
            Racer.downleft = game.transform.rotate(Racer.right, -135)

        self.direction = direction
        self.set_direction(direction)
        self.image = Racer.image
        self.time_spent_waiting = 0
        Racer.speed = speed
        self.speed = speed
        self.rect = self.image.get_rect()
        self.timer = 0
        self.timer_on = False

        #make sure it is in the appropriate location
        self.rect.topleft = location
        #get the width & height of screen
        self.width = screensize[0]
        self.height = screensize[1]
        self.x = location[0]
        self.y = location[1]
        self.movements = move_array
        self.current_move = 0
        self.old_pos_x = location[0]
        self.old_pos_y = location[1]
        #This variable keeps track of the number of cycles
        #the enemy has waited before restarting
        #If 0, enemy continues as normal
        #Enemy will stay stopped until stop_time == max_stop_time
        self.stop_time = 0

    # this is the update method with a parameter - it ensures the Enemy is
    # facing opposite dir of the Player then updates
    def update(self, interval, player_coordinates):
        self.move(interval)
        if self.timer_on:
            self.timer += 1

    def get_strength(self):
        return 3

    #this moves the Enemy to where he is supposed to be based on the direction
    '''
    Note : We wrote this function interpreting 'look' to mean the direction
    in which the Enemy is facing.
    Please have pity on our souls for the duplicated/relatively ugly
    code...not currently being used.
    '''

    def move(self, interval):
        #If the stop_time is max_stop_time, then the enemy waited long enough
        #and can restart moving
        #If the stop_time is 0, it indicates that the car can continue moving
        if self.stop_time == self.max_stop_time or self.stop_time == 0:
            #Make sure stop time is back at 0 once we are moving again
            self.stop_time = 0
            curr_action = self.movements[self.current_move]
            distance_moved_x = fabs(self.old_pos_x - self.x)
            distance_moved_y = fabs(self.old_pos_y - self.y)
            if (curr_action[0:1] == "s"):
                self.speed = 0
            if (curr_action[0:1] == "p"):
                self.speed = 0
                if self.time_spent_waiting > float(curr_action[1:]):
                    self.speed = Racer.speed
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.time_spent_waiting = 0
                else:
                    self.time_spent_waiting += 1

            if (curr_action[0:1] == "d"):
                self.y += self.speed * interval
                self.direction = "down"
                self.set_direction("down")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_y > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_y = self.y

            elif (curr_action[0:1] == "r"):
                self.x += self.speed * interval
                self.direction = "right"
                self.set_direction("right")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_x > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_x = self.x

            elif (curr_action[0:1] == "u"):
                self.y -= self.speed * interval
                self.direction = "up"
                self.set_direction("up")
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_y > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_y = self.y

            elif (curr_action[0:1] == "l"):
                self.direction = "left"
                self.set_direction("left")
                self.x -= self.speed * interval
                #Must reset rect after direction change
                self.rect = self.image.get_rect(center=self.rect.center)
                if distance_moved_x > float(curr_action[1:]):
                    if (self.current_move == len(self.movements) - 1):
                        self.current_move = 0
                    else:
                        self.current_move += 1
                    self.old_pos_x = self.x

        else:
            #add one to the number of cycles the enemy has waited
            self.stop_time += 1

    #Used to calculate how long it's been since enemy crossed finish
    def start_timer(self):
        self.timer_on = True

    #method to set the direction
    def set_direction(self, direction):
        #set the image based on the direction
        if direction == "right":
            self.image = Racer.right
        elif direction == "downright":
            self.image = Racer.downright
        elif direction == "down":
            self.image = Racer.down
        elif direction == "downleft":
            self.image = Racer.downleft
        elif direction == "left":
            self.image = Racer.left
        elif direction == "upleft":
            self.image = Racer.upleft
        elif direction == "up":
            self.image = Racer.up
        elif direction == "upright":
            self.image = Racer.upright

    def stop(self):
        #Once stop_time is > 0, the enemy will stop
        #Enemy will continue to be stopped until
        #The cycle count reaches our max_stop_time
        #Move function takes care of restarting enemy
        self.stop_time = 1

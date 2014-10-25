import pygame as game
from states.Constants import Constants
import util.SpriteSheet as SS
import Tile
import math


class Player(game.sprite.Sprite):
    #Variables for the images
    stopped = None
    accelerating = None
    full_speed = None
    crash = None

    #Used in setting the image
    FRAME_SLOW = 10

    # Constructor for our Player takes an initial location, the dimensions of
    # the screen, and the speed

    def __init__(self, location, screensize, temp_map, enemy):

        game.sprite.Sprite.__init__(self)

        #set intitial location to passed parameter
        self.x = location[0]
        self.y = location[1]
        #Get the screensize from the parameter
        Player.screen_width = screensize[0]
        Player.screen_height = screensize[1]
        #Set initial direction of the car
        self.direction = "right"
        #Set the map for the player to use to get tiles
        self.map = temp_map
        #Enemies being passed to car, very bad right now
        self.enemies = enemy

        #Set our starting health
        self.health = Constants.PLAYER_STARTING_HEALTH
        #create health variable for knowing where our health is e.g quarter
        self.current_health = None
        self.damage = 0

        #set the sounds and images for our car
        self.set_sounds()
        self.set_images()

        # initialize image array shit, can Tuvia make this a little cleaner?
        self.imageArray = Player.stopped
        Player.right = self.imageArray
        self.image = self.imageArray[0]
        self.rect = self.image.get_rect()
        #Set rect center to be at the passed coordinates
        self.rect.center = location
        #We can only run set rotations after we set our first image
        self.set_rotations()

        #Set our acceleration states
        self.accelerationState = "stopped"

        #Not sure what these frame variables are for are for
        self.frame = 0
        self.frameCalls = 0
        self.set_image()

        #Set difficulty variable which makes dying easier?
        self.difficulty = Constants.DIFFICULTY

        #Set starting speed and acceleration
        self.speed = Constants.PLAYER_MIN_SPEED
        self.is_accelerating = False

        #Used to see if our direction has changed
        self.dir_changed = False

        #Create garage variable
        self.garage = None

    #Method to set the images for the player if they have not been set
    def set_images(self):
        if Player.stopped is None:
            tmp = SS.loadSheet("images/sprites/player_animations.png",
                               52, 26, [8, 1])
            tmp = tmp[0]
            Player.stopped = []
            Player.stopped.append(tmp[0])
        if Player.accelerating is None:
            tmp = SS.loadSheet("images/sprites/player_animations.png",
                               52, 26, [8, 1])
            tmp = tmp[0]
            Player.accelerating = []
            for i in range(1, 5):
                Player.accelerating.append(tmp[i])
        if Player.full_speed is None:
            tmp = SS.loadSheet("images/sprites/player_animations.png",
                               52, 26, [8, 1])
            tmp = tmp[0]
            Player.full_speed = []
            for i in range(5, len(tmp)):
                Player.full_speed.append(tmp[i])

    #Method to set the sounds if they have not been set
    def set_sounds(self):
        if Player.crash is None:
            Player.crash = game.mixer.Sound("audio/car_screech.wav")

    #Returns strength of this car for collision detection purposes
    def get_strengths(self):
        return 1

    # Update method
    def update(self, interval):
        #Initially the direction has not changed
        self.dir_changed = False

        #Initially assume we are slowing down
        acceleration = -Constants.PLAYER_ACCELERATION
        #Get the keys pressed
        keys_pressed = game.key.get_pressed()
        if keys_pressed[game.K_LEFT] and keys_pressed[game.K_UP]:
            # change of direction, stop playing crash sound & set the direction
            if self.direction != "upleft":
                self.dir_changed = True
                self.set_direction("upleft")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_LEFT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downleft":
                self.dir_changed = True
                self.set_direction("downleft")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_LEFT]:
            if self.direction != "left":
                self.dir_changed = True
                self.set_direction("left")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_UP]:
            if self.direction != "upright":
                self.dir_changed = True
                self.set_direction("upright")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downright":
                self.dir_changed = True
                self.set_direction("downright")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_RIGHT]:
            if self.direction != "right":
                self.dir_changed = True
                self.set_direction("right")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_UP]:
            if self.direction != "up":
                self.dir_changed = True
                self.set_direction("up")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_DOWN]:
            if self.direction != "down":
                self.dir_changed = True
                self.set_direction("down")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        #Check if the new speed will put us over or under our max/min
        #Before we set the speed
        if self.speed + acceleration * interval >\
                Constants.PLAYER_MAX_SPEED:
            self.speed = Constants.PLAYER_MAX_SPEED
        elif self.speed + acceleration * interval <\
                Constants.PLAYER_MIN_SPEED:
            self.speed = Constants.PLAYER_MIN_SPEED
        else:
            self.speed += acceleration * interval

        #Set our car image based on whether it is
        #stopped, accelerating, or decelerating
        self.set_acceleration_image(acceleration)

        #Call our move function
        self.move(interval)

    def check_key(self, key):
        index = 0
        for k in key:
            if self.rect.colliderect(k.rect):
                return (k, index)
            index += 1
        return None

    def check_garage(self, garage):
        for g in garage:
            self.garage = g
            if g.isOpened() and self.rect.colliderect(g.rect):
                return True
        return False

    #Moves player depending on whether or not he has collided with an object
    def move(self, interval):
        #Create variable to calculate damage to be done
        damage_to_do = 0
        #Set flag to indicate whether or not we have fixed the collision yet
        collision_fixed = False

        #Get the rectangles from the map around the x,y position of the car
        wall_rects = self.map.get_tiles(self.x, self.y)
        #Add the enemy rectangle to our array
        for enemy in self.enemies:
            wall_rects.append(enemy)

        #Go through all of the collidable rects around the player
        for r in wall_rects:
            #A strength > 0 indicates a collidable object
            if r.get_strength() > 0:
                #This same if statement is repeated for all midpoints
                #Checking if the midpoint of the car is in the other rect
                #This midpoint check tells us how to fix the car's position
                if (r.rect.collidepoint(self.rect.midbottom)):
                    damage_to_do = r.get_strength()
                    self.rect.bottom = r.rect.top
                    collision_fixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.y -= .01
                if (r.rect.collidepoint(self.rect.midleft)):
                    damage_to_do = r.get_strength()
                    self.rect.left = r.rect.right
                    collision_fixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01
                if (r.rect.collidepoint(self.rect.midright)):
                    damage_to_do = r.get_strength()
                    self.rect.right = r.rect.left
                    collision_fixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (r.rect.collidepoint(self.rect.midtop)):
                    damage_to_do = r.get_strength()
                    self.rect.top = r.rect.bottom
                    collision_fixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.y += .01

                #These collision if statements are to fix hitting any corners
                #Only happens if there wasnt a collision with one of the
                #centers of the car
                if (not collision_fixed and r.rect.collidepoint(
                        self.rect.topright)):
                    damage_to_do = r.get_strength()
                    collision_fixed = True
                    self.rect.right = r.rect.left
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (not collision_fixed and r.rect.collidepoint(
                        self.rect.bottomright)):
                    damage_to_do = r.get_strength()
                    collision_fixed = True
                    self.rect.right = r.rect.left
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (not collision_fixed and r.rect.collidepoint(
                        self.rect.topleft)):
                    damage_to_do = r.get_strength()
                    collision_fixed = True
                    self.rect.left = r.rect.right
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01
                if (not collision_fixed and r.rect.collidepoint(
                        self.rect.bottomleft)):
                    damage_to_do = r.get_strength()
                    collision_fixed = True
                    self.rect.left = r.rect.right
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01

        if collision_fixed:
            self.damage += damage_to_do
            Player.crash.play()
        #If the collision wasnt fixed then allow the player to move
        else:
            if self.direction == "upleft":
                self.x -= self.speed * interval * .7071  # 1/Sqrt 2
                self.y -= self.speed * interval * .7071
            if self.direction == "downleft":
                self.x -= self.speed * interval * .7071
                self.y += self.speed * interval * .7071
            if self.direction == "left":
                self.x -= self.speed * interval
            if self.direction == "upright":
                self.x += self.speed * interval * .7071
                self.y -= self.speed * interval * .7071
            if self.direction == "downright":
                self.x += self.speed * interval * .7071
                self.y += self.speed * interval * .7071
            if self.direction == "right":
                self.x += self.speed * interval
            if self.direction == "up":
                self.y -= self.speed * interval
            if self.direction == "down":
                self.y += self.speed * interval

    #Based on the acceleration given and the current acceleration state
    #Will set the next acceleration state and change the car's image
    def set_acceleration_image(self, accel):
        if self.accelerationState == "stopped":
            if self.speed != Constants.PLAYER_MIN_SPEED:
                self.accelerationState = "accelerating"
                self.set_image_array()
        elif self.accelerationState == "accelerating":
            if self.speed == Constants.PLAYER_MAX_SPEED:
                self.accelerationState = "maxed"
                self.set_image_array()
            elif accel < 0:
                self.accelerationState = "slowing"
                self.set_image_array()
        elif self.accelerationState == "slowing":
            if self.speed == Constants.PLAYER_MIN_SPEED:
                self.accelerationState = "stopped"
                self.set_image_array()
            elif accel > 0:
                self.accelerationState = "accelerating"
                self.set_image_array()
        elif self.accelerationState == "maxed":
            if self.speed < Constants.PLAYER_MAX_SPEED:
                self.accelerationState = "slowing"
                self.set_image_array()

        self.set_image()

    #Sets the image array based on the acceleration state
    def set_image_array(self):
        if self.accelerationState == "stopped":
            Player.right = Player.stopped
        elif self.accelerationState == "accelerating":
            Player.right = Player.accelerating
        elif self.accelerationState == "maxed":
            Player.right = Player.full_speed
        elif self.accelerationState == "slowing":
            Player.right = Player.stopped
        self.set_rotations()

    #Sets all of the rotations for the player
    def set_rotations(self):
        Player.left = SS.rotateSprites(Player.right, 180)
        Player.up = SS.rotateSprites(Player.right, 90)
        Player.down = SS.rotateSprites(Player.right, -90)
        Player.upright = SS.rotateSprites(Player.right, 45)
        Player.upleft = SS.rotateSprites(Player.right, 135)
        Player.downright = SS.rotateSprites(Player.right, -45)
        Player.downleft = SS.rotateSprites(Player.right, -135)
        self.set_direction(self.direction)
        self.frame = 0

    def set_direction(self, direction):
        self.direction = direction
        # set the image based on the direction
        if direction == "right":
            self.imageArray = Player.right
        elif direction == "downright":
            self.imageArray = Player.downright
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "down":
            self.imageArray = Player.down
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "downleft":
            self.imageArray = Player.downleft
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "left":
            self.imageArray = Player.left
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "upleft":
            self.imageArray = Player.upleft
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "up":
            self.imageArray = Player.up
            # self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "upright":
            self.imageArray = Player.upright
            # self.rect = self.image.get_rect(center=self.rect.center)

    #Calculates our player's health
    def calculate_health(self):
        self.health = Constants.PLAYER_STARTING_HEALTH - (
            self.damage / (10 * (11 - self.difficulty)))
        if not self.current_health == "quarter" and self.health < 25:
            self.current_health = "quarter"
        elif not self.current_health == "half" and 25 < self.health < 75:
            self.current_health = "half"
        elif not self.current_health == "half" and self.health > 75:
            self.current_health = "full"
        return self.health

    def heal(self):
        self.damage -= 150
        if self.damage < 0:
            self.damage = 0

    def check_health(self, pack):
        index = 0
        for p in pack:
            if self.rect.colliderect(p.rect):
                return (p, index)
            index += 1
        return None

    def set_image_rotations(self, healthlevel):
        if healthlevel == "half":
            Player.image = Player.half_health
        elif healthlevel == "quarter":
            Player.image = Player.quarter_health
        else:
            Player.image = Player.full_health
        Player.rect = Player.image.get_rect()
        Player.right = Player.image
        Player.left = game.transform.rotate(Player.right, 180)
        Player.up = game.transform.rotate(Player.right, 90)
        Player.down = game.transform.rotate(Player.right, -90)
        Player.upright = game.transform.rotate(Player.right, 45)
        Player.upleft = game.transform.rotate(Player.right, 135)
        Player.downright = game.transform.rotate(Player.right, -45)
        Player.downleft = game.transform.rotate(Player.right, -135)
        self.set_direction(self.direction)

    def set_image(self):
        self.image = self.imageArray[self.frame]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.frameCalls += 1
        if self.frameCalls % Player.FRAME_SLOW == 0:
            self.frame += 1
        if self.frame >= len(self.imageArray):
            self.frame = 0

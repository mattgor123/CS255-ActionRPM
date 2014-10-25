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
        #Enemy being passed to car, very bad right now
        self.enemy = enemy

        #Set our starting health
        self.health = Constants.PLAYER_STARTING_HEALTH
        #create health variable for knowing where our health is e.g. wuarter/half/etc?
        self.current_health = None
        self.damage = 0
        #Create array that holds wall rectangles for collision
        self.wall_rects = None

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

    def get_strengths(self):
        return 1

    # update method moves the sprite & possibly changes its image based on the
    # keypress
    def update(self, interval):
        self.dir_changed = False
        tmp = self.direction
        keys_pressed = game.key.get_pressed()
        if keys_pressed[game.K_LEFT] and keys_pressed[game.K_UP]:
            # change of direction, stop playing crash sound & set the direction
            if self.direction != "upleft":
                self.dir_changed = True
                self.set_direction("upleft")
                Player.crash.stop()
            self.is_accelerating = True
            # check for collision with top or left

        elif keys_pressed[game.K_LEFT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downleft":
                self.dir_changed = True
                self.set_direction("downleft")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_LEFT]:
            if self.direction != "left":
                self.dir_changed = True
                self.set_direction("left")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_UP]:
            if self.direction != "upright":
                self.dir_changed = True
                self.set_direction("upright")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downright":
                self.dir_changed = True
                self.set_direction("downright")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT]:
            if self.direction != "right":
                self.dir_changed = True
                self.set_direction("right")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_UP]:
            if self.direction != "up":
                self.dir_changed = True
                self.set_direction("up")
                Player.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_DOWN]:
            if self.direction != "down":
                self.dir_changed = True
                self.set_direction("down")
                Player.crash.stop()
            self.is_accelerating = True

        else:
            self.is_accelerating = False

        if self.is_accelerating is True:
            acceleration = Constants.PLAYER_ACCELERATION
        else:
            acceleration = -Constants.PLAYER_ACCELERATION

        self.speed += acceleration * interval

        if self.speed > Constants.PLAYER_MAX_SPEED:
            self.speed = Constants.PLAYER_MAX_SPEED
        if self.speed < Constants.PLAYER_MIN_SPEED:
            self.speed = Constants.PLAYER_MIN_SPEED
        self.check_acceleration_state(acceleration)
        self.set_image()
        self.wall_rects = self.map.get_tiles(self.x, self.y)
        self.wall_rects.append(self.enemy)
        if self.garage is not None:
            self.wall_rects.append(self.garage)
        return self.move(interval)

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

    def move(self, interval):
        #if self.should_move(Player.wall_rects, [], interval):
        #Do something
        damage_to_do = 0
        collisionFixed = False
        for r in self.wall_rects:
            if r.get_strength() > 0:
                if (r.rect.collidepoint(self.rect.midbottom)):
                    damage_to_do = r.get_strength()
                    self.rect.bottom = r.rect.top
                    collisionFixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.y -= .01
                if (r.rect.collidepoint(self.rect.midleft)):
                    damage_to_do = r.get_strength()
                    self.rect.left = r.rect.right
                    collisionFixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01
                if (r.rect.collidepoint(self.rect.midright)):
                    damage_to_do = r.get_strength()
                    self.rect.right = r.rect.left
                    collisionFixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (r.rect.collidepoint(self.rect.midtop)):
                    damage_to_do = r.get_strength()
                    self.rect.top = r.rect.bottom
                    collisionFixed = True
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.y += .01
                    #These collisions are to fix hitting any corners
                    #Only happens if there wasnt a collision with one of the
                    #centers of the car
                if (not collisionFixed and r.rect.collidepoint(
                        self.rect.topright)):
                    damage_to_do = r.get_strength()
                    collisionFixed = True
                    self.rect.right = r.rect.left
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (not collisionFixed and r.rect.collidepoint(
                        self.rect.bottomright)):
                    damage_to_do = r.get_strength()
                    collisionFixed = True
                    self.rect.right = r.rect.left
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x -= .01
                if (not collisionFixed and r.rect.collidepoint(
                        self.rect.topleft)):
                    damage_to_do = r.get_strength()
                    collisionFixed = True
                    self.rect.left = r.rect.right
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01
                if (not collisionFixed and r.rect.collidepoint(
                        self.rect.bottomleft)):
                    damage_to_do = r.get_strength()
                    collisionFixed = True
                    self.rect.left = r.rect.right
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.x += .01

        if collisionFixed:
            self.damage += damage_to_do
            Player.crash.play()

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

        return collisionFixed

    def should_move(self, tempRect, walls):
        real_walls = game.sprite.Group()
        for r in walls:
            if r.isCollidable():
                real_walls.add(r)
        hit_list = game.sprite.spritecollide(self, real_walls, False)
        if len(hit_list) > 1:
            print ((hit_list[0].x, hit_list[0].y))
            print "Total collisions = " + str(len(hit_list))
            return False
        return True

    def is_point_in_rect(self, rect, p_x, p_y):
        min_x = rect[0]
        min_y = rect[1]
        max_x = rect[2]
        max_y = rect[3]
        return (min_x < p_x and min_y < p_y and
                max_x > p_x and max_y > p_y)

    def check_player_wall_collision(self, wall, tempRect):
        player_rect = tempRect
        x_offset = player_rect.width / (Tile.Tile.WIDTH * 1.0)
        y_offset = player_rect.height / (Tile.Tile.HEIGHT * 1.0)
        player_min_x = math.floor(self.x)
        player_min_y = math.floor(self.y)
        player_max_x = math.floor(self.x + x_offset)
        player_max_y = math.floor(self.y + y_offset)
        coords = (player_min_x, player_min_y, player_max_x, player_max_y)
        return self.is_point_in_rect(coords, wall.x, wall.y)

    def check_acceleration_state(self, accel):
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

    def calculate_health(self):
        self.health = Constants.PLAYER_STARTING_HEALTH - (
            self.damage / (10 * (11 - self.difficulty)))
        if self.health < 25 and not self.current_health == "quarter":
            self.current_health = "quarter"
        elif 25 < self.health < 75 and not self.current_health == \
                "half":
            self.current_health = "half"
        elif self.health > 75 and not self.current_health == "full":
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

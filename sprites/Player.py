import pygame as game
from states.Constants import Constants
import util.SpriteSheet as SS
import sprites.Fireball as Fireball


# TODO : Player health animation doesnt change until ya let go of arrow key
class Player(game.sprite.Sprite):
    #Variables for the images
    full_stopped = None
    full_accelerating = None
    full_full_speed = None
    half_stopped = None
    half_accelerating = None
    half_full_speed = None
    quar_stopped = None
    quar_accelerating = None
    quar_full_speed = None
    crash = None

    #Used in setting the image
    FRAME_SLOW = 10

    # Constructor for our Player takes an initial location, the dimensions of
    # the screen, and the speed

    def __init__(self, location, screensize):

        game.sprite.Sprite.__init__(self)

        #set intitial location to passed parameter
        self.x = location[0]
        self.y = location[1]
        #Get the screensize from the parameter
        Player.screen_width = screensize[0]
        Player.screen_height = screensize[1]
        #Set initial direction of the car
        self.direction = "right"

        #Inventory initialized as empty
        self.inventory = []

        #Set our starting health
        self.health = Constants.PLAYER_STARTING_HEALTH
        #create health variable for knowing where our health is e.g quarter
        self.current_health = None
        self.damage = 0

        #set the sounds and images for our car
        self.set_sounds()
        self.set_images()

        # initialize image array shit, can Tuvia make this a little cleaner?
        self.imageArray = Player.full_stopped
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

        self.score = Constants.START_SCORE

        self.fire_rate = 30
        self.projectiles = game.sprite.Group()

    #Method to add an item to a player's inventory
    def grab(self, item):
        self.score += item.points
        if item.name == "healthpack":
            self.heal(30)
            return
        self.inventory.append(item.name)

    def _get_stopped(self, which):
        tmp = SS.loadSheet("images/sprites/player_total.png",
                           52, 26, [8, 3])
        tmp = tmp[which]
        return [tmp[0]]

    def _get_accelerating(self, which):
        tmp = SS.loadSheet("images/sprites/player_total.png",
                           52, 26, [8, 3])
        tmp = tmp[which]
        accelerating = []
        for i in range(1, 5):
            accelerating.append(tmp[i])
        return accelerating

    def _get_full(self, which):
        tmp = SS.loadSheet("images/sprites/player_total.png",
                           52, 26, [8, 3])
        tmp = tmp[which]
        full_speed = []
        for i in range(5, len(tmp)):
            full_speed.append(tmp[i])
        return full_speed

    #Method to set the images for the player if they have not been set
    def set_images(self):
        if Player.full_stopped is None:
            Player.full_stopped = self._get_stopped(0)
        if Player.full_accelerating is None:
            Player.full_accelerating = self._get_accelerating(0)
        if Player.full_full_speed is None:
            Player.full_full_speed = self._get_full(0)
        if Player.half_stopped is None:
            Player.half_stopped = self._get_stopped(1)
        if Player.half_accelerating is None:
            Player.half_accelerating = self._get_accelerating(1)
        if Player.half_full_speed is None:
            Player.half_full_speed = self._get_full(1)
        if Player.quar_stopped is None:
            Player.quar_stopped = self._get_stopped(2)
        if Player.quar_accelerating is None:
            Player.quar_accelerating = self._get_accelerating(2)
        if Player.quar_full_speed is None:
            Player.quar_full_speed = self._get_full(2)

    #Method to set the sounds if they have not been set
    def set_sounds(self):
        if Player.crash is None:
            Player.crash = game.mixer.Sound("audio/car_screech.wav")

    #Returns strength of this car for collision detection purposes
    def get_strength(self):
        return 1

    # Update method
    def update(self, interval):
        #Initially the direction has not changed
        self.dir_changed = False

        #Initially assume we are slowing down
        acceleration = -2 * Constants.PLAYER_ACCELERATION
        #Get the keys pressed
        keys_pressed = game.key.get_pressed()
        if keys_pressed[game.K_a] and keys_pressed[game.K_w]:
            # change of direction, stop playing crash sound & set the direction
            if self.direction != "upleft":
                self.dir_changed = True
                self.set_direction("upleft")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_a] and keys_pressed[game.K_s]:
            if self.direction != "downleft":
                self.dir_changed = True
                self.set_direction("downleft")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_a]:
            if self.direction != "left":
                self.dir_changed = True
                self.set_direction("left")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_d] and keys_pressed[game.K_w]:
            if self.direction != "upright":
                self.dir_changed = True
                self.set_direction("upright")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_d] and keys_pressed[game.K_s]:
            if self.direction != "downright":
                self.dir_changed = True
                self.set_direction("downright")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_d]:
            if self.direction != "right":
                self.dir_changed = True
                self.set_direction("right")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_w]:
            print self.x
            print self.y
            if self.direction != "up":
                self.dir_changed = True
                self.set_direction("up")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        elif keys_pressed[game.K_s]:
            if self.direction != "down":
                self.dir_changed = True
                self.set_direction("down")
                Player.crash.stop()
            acceleration = Constants.PLAYER_ACCELERATION

        if keys_pressed[game.KMOD_SHIFT]:
            self.breaking = True
            acceleration = -4 * Constants.PLAYER_ACCELERATION

        #Check if the new speed will put us over or under our max/min
        #Before we set the speed
        if self.speed + acceleration * interval > \
                Constants.PLAYER_MAX_SPEED:
            self.speed = Constants.PLAYER_MAX_SPEED
        elif self.speed + acceleration * interval < \
                Constants.PLAYER_MIN_SPEED:
            self.speed = Constants.PLAYER_MIN_SPEED
        else:
            self.speed += acceleration * interval

        #Set our car image based on whether it is
        #stopped, accelerating, or decelerating
        self.set_acceleration_image(acceleration)

        self.score -= interval * 10

        #Call our move function
        self.move(interval)

        for projectile in self.projectiles:
            projectile.update(interval, [0, 0])

    #Moves player depending on whether or not he has collided with an object
    def move(self, interval):
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

    #Hacky method to determine if we should win...will rethink this, but for
    # assignment it's fine I think
    def has_beaten_level(self, level):
        if level == 0:
            if self.y <= 2:
                return True
            else:
                return False
        else:
            return False

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
        if self.current_health == "full":
            if self.accelerationState == "stopped":
                Player.right = Player.full_stopped
            elif self.accelerationState == "accelerating":
                Player.right = Player.full_accelerating
            elif self.accelerationState == "maxed":
                Player.right = Player.full_full_speed
            elif self.accelerationState == "slowing":
                Player.right = Player.full_stopped
        elif self.current_health == "half":
            if self.accelerationState == "stopped":
                Player.right = Player.half_stopped
            elif self.accelerationState == "accelerating":
                Player.right = Player.half_accelerating
            elif self.accelerationState == "maxed":
                Player.right = Player.half_full_speed
            elif self.accelerationState == "slowing":
                Player.right = Player.half_stopped
        elif self.current_health == "quarter":
            if self.accelerationState == "stopped":
                Player.right = Player.quar_stopped
            elif self.accelerationState == "accelerating":
                Player.right = Player.quar_accelerating
            elif self.accelerationState == "maxed":
                Player.right = Player.quar_full_speed
            elif self.accelerationState == "slowing":
                Player.right = Player.quar_stopped
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
        self.health -= (self.damage / 10.0)
        self.damage = 0
            # Constants.PLAYER_STARTING_HEALTH - (
            # self.damage / (10 * (11 - self.difficulty)))
        if not self.current_health == "quarter" and self.health < 25:
            self.current_health = "quarter"
        elif not self.current_health == "half" and 25 < self.health < 75:
            self.current_health = "half"
        elif not self.current_health == "half" and self.health > 75:
            self.current_health = "full"
        return self.health

    def heal(self, amount):
        self.health += amount
        if self.health > Constants.PLAYER_STARTING_HEALTH:
            self.health = Constants.PLAYER_STARTING_HEALTH

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

    def get_coordinates(self):
        return [self.x, self.y]

    def set_coordinates(self, coors):
        self.x = coors[0]
        self.y = coors[1]

    def shoot(self):
        if "fireball" not in self.inventory:
            return
        self.projectiles.add(
            Fireball.Fireball(
                Constants.PLAYER_MAX_SPEED + 10,
                self.direction, [self.x,self.y], 300,50))
        self.score -= 100

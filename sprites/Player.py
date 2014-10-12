import pygame as game
from states.Constants import Constants
import util.SpriteSheet as SS


class Player(game.sprite.Sprite):
    # These are the images
    # full_health = None
    # half_health = None
    # quarter_health = None
    stopped = None
    accelerating = None
    full_speed = None
    crash = None
    current = None
    max_speed = Constants.PLAYER_MAX_SPEED
    wall_rects = None
    FRAME_SLOW = 10

    # Constructor for our Player takes an initial location, the dimensions of
    # the screen, and the speed

    def __init__(self, location, screensize, difficulty):

        game.sprite.Sprite.__init__(self)
        Player.screen_width = screensize[0]
        Player.screen_height = screensize[1]
        self.direction = "right"
        # set the images to the appropriate ones based on the direction of the
        # character
        # if Player.full_health is None:
        # Player.full_health = game.image.load(
        #         "images/sprites/playerfullhealth.png").convert_alpha()
        if Player.crash is None:
            Player.crash = game.mixer.Sound("audio/car_screech.wav")
        # if Player.half_health is None:
        #     Player.half_health = game.image.load(
        #         "images/sprites/playerhalfhealth.png").convert_alpha()
        # if Player.quarter_health is None:
        #     Player.quarter_health = game.image.load(
        #         "images/sprites/playerquarterhealth.png").convert_alpha()

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
        # initialize
        self.imageArray = Player.stopped
        Player.right = self.imageArray
        self.image = self.imageArray[0]
        self.rect = self.image.get_rect()

        self.accelerationState = "stopped"
        self.set_rotations()
        self.frame = 0
        self.frameCalls = 0
        self.set_image()
        self.crash = Player.crash
        self.damage = 0
        self.health = Constants.PLAYER_STARTING_HEALTH
        # self.set_image_rotations(self.health)
        self.speed = Constants.PLAYER_MIN_SPEED
        self.is_accelerating = False
        self.rect.center = location
        self.screen_width = Player.screen_width
        self.screen_height = Player.screen_height
        self.dir_changed = False
        self.difficulty = difficulty
        #self.has_initialized = True

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
                self.crash.stop()
            self.is_accelerating = True
            # check for collision with top or left

        elif keys_pressed[game.K_LEFT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downleft":
                self.dir_changed = True
                self.set_direction("downleft")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_LEFT]:
            if self.direction != "left":
                self.dir_changed = True
                self.set_direction("left")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_UP]:
            if self.direction != "upright":
                self.dir_changed = True
                self.set_direction("upright")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downright":
                self.dir_changed = True
                self.set_direction("downright")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_RIGHT]:
            if self.direction != "right":
                self.dir_changed = True
                self.set_direction("right")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_UP]:
            if self.direction != "up":
                self.dir_changed = True
                self.set_direction("up")
                self.crash.stop()
            self.is_accelerating = True

        elif keys_pressed[game.K_DOWN]:
            if self.direction != "down":
                self.dir_changed = True
                self.set_direction("down")
                self.crash.stop()
            self.is_accelerating = True

        else:
            self.is_accelerating = False

        if self.is_accelerating is True:
            acceleration = Constants.PLAYER_ACCELERATION
        else:
            acceleration = -Constants.PLAYER_ACCELERATION

        self.speed += acceleration * interval

        if self.speed > Player.max_speed:
            self.speed = Player.max_speed
        if self.speed < Constants.PLAYER_MIN_SPEED:
            self.speed = Constants.PLAYER_MIN_SPEED
        self.check_acceleration_state(acceleration)
        self.set_image()
        self.can_move = True
        # self.check_collision(tmp)
        if self.can_move:
            self.move(interval)

    def check_collision(self, old):
        for r in Player.wall_rects:
            if self.rect.colliderect(r) \
                    and self.speed > Constants.PLAYER_MIN_SPEED:
                self.set_direction(old)
                self.set_image()
                break

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
        if self.health < 25 and not self.current == "quarter":
            self.current = "quarter"
        elif 25 < self.health < 75 and not self.current == \
                "half":
            self.current = "half"
        elif self.health > 75 and not self.current == "full":
            self.current = "full"
        return self.health

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

    def move(self, interval):
        pass
    #     is_collision = False
    #     for r in Player.wall_rects:
    #         if self.rect.colliderect(r):
    #             if (self.speed != Constants.PLAYER_MIN_SPEED):
    #                 self.speed = Constants.PLAYER_MIN_SPEED
    #                 # self.damage += 5
    #                 collisionFixed = False
    #                 if (r.collidepoint(self.rect.midbottom)):
    #                     self.rect.bottom = r.top
    #                     collisionFixed = True
    #                 if (r.collidepoint(self.rect.midleft)):
    #                     self.rect.left = r.right
    #                     collisionFixed = True
    #                 if (r.collidepoint(self.rect.midright)):
    #                     self.rect.right = r.left
    #                     collisionFixed = True
    #                 if (r.collidepoint(self.rect.midtop)):
    #                     self.rect.top = r.bottom
    #                     collisionFixed = True

    #                 #These collisions are to fix hitting any corners
    #                 #Only happens if there wasnt a collision with one
    #                 #of the centers of the car
    #                 if (not collisionFixed
    #                         and r.collidepoint(self.rect.topright)):
    #                     self.rect.right = r.left
    #                 if (not collisionFixed
    #                         and r.collidepoint(self.rect.bottomright)):
    #                     self.rect.right = r.left
    #                 if (not collisionFixed
    #                         and r.collidepoint(self.rect.topleft)):
    #                     self.rect.left = r.right
    #                 if (not collisionFixed
    #                         and r.collidepoint(self.rect.bottomleft)):
    #                     self.rect.left = r.right

    #                         #self.crash.play()

    #     if self.direction == "upleft":
    #         self.rect = self.rect.move(-self.speed * interval,
    #                                    -self.speed * interval)
    #     if self.direction == "downleft":
    #         self.rect = self.rect.move(-self.speed * interval,
    #                                    +self.speed * interval)
    #     if self.direction == "left":
    #         self.rect = self.rect.move(-self.speed * interval, 0)
    #     if self.direction == "upright":
    #         self.rect = self.rect.move(self.speed * interval,
    #                                    -self.speed * interval)
    #     if self.direction == "downright":
    #         self.rect = self.rect.move(self.speed * interval,
    #                                    self.speed * interval)
    #     if self.direction == "right":
    #         self.rect = self.rect.move(self.speed * interval, 0)
    #     if self.direction == "up":
    #         self.rect = self.rect.move(0, -self.speed * interval)
    #     if self.direction == "down":
    #         self.rect = self.rect.move(0, self.speed * interval)

    # def add_walls(self, wrects):
    #     Player.wall_rects = wrects

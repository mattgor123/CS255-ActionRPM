import pygame as game
from states.Constants import Constants


class Player(game.sprite.Sprite):
    # These are the images
    full_health = None
    half_health = None
    quarter_health = None
    crash = None
    current = None
    max_speed = Constants.PLAYER_MAX_SPEED
    wall_rects = None
    last_move_1 = ""

    # Constructor for our Player takes an initial location, the dimensions of
    # the screen, and the speed

    def __init__(self, location, screensize, difficulty):

        game.sprite.Sprite.__init__(self)
        Player.screen_width = screensize[0]
        Player.screen_height = screensize[1]
        self.direction = "right"
        # set the images to the appropriate ones based on the direction of the
        # character
        if Player.full_health is None:
            Player.full_health = game.image.load(
                "images/sprites/playerfullhealth.png").convert_alpha()
        if Player.crash is None:
            Player.crash = game.mixer.Sound("audio/car_screech.wav")
        if Player.half_health is None:
            Player.half_health = game.image.load(
                "images/sprites/playerhalfhealth.png").convert_alpha()
        if Player.quarter_health is None:
            Player.quarter_health = game.image.load(
                "images/sprites/playerquarterhealth.png").convert_alpha()
        # initialize
        self.image = Player.full_health
        self.crash = Player.crash
        self.damage = 0
        self.health = Constants.PLAYER_STARTING_HEALTH
        self.set_image_rotations(self.health)
        self.speed = Constants.PLAYER_MIN_SPEED
        self.is_accelerating = False
        self.rect = self.image.get_rect()
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

        self.speed = self.speed + acceleration*interval

        if self.speed > Player.max_speed:
            self.speed = Player.max_speed
        if self.speed < Constants.PLAYER_MIN_SPEED:
            self.speed = Constants.PLAYER_MIN_SPEED
        self.move(interval)

    def set_direction(self, direction):
        self.direction = direction
        # set the image based on the direction
        if direction == "right":
            self.image = Player.right
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "downright":
            self.image = Player.downright
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "down":
            self.image = Player.down
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "downleft":
            self.image = Player.downleft
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "left":
            self.image = Player.left
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "upleft":
            self.image = Player.upleft
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "up":
            self.image = Player.up
            self.rect = self.image.get_rect(center=self.rect.center)
        elif direction == "upright":
            self.image = Player.upright
            self.rect = self.image.get_rect(center=self.rect.center)

    def calculate_health(self):
        self.health = Constants.PLAYER_STARTING_HEALTH - (
            self.damage / (10 * (11 - self.difficulty)))
        if self.health < 25 and not self.current == "quarter":
            self.current = "quarter"
            self.set_image_rotations("quarter")
        elif 25 < self.health < 75 and not self.current == \
                "half":
            self.current = "half"
            self.set_image_rotations("half")
        elif self.health > 75 and not self.current == "full":
            self.current = "full"
            self.set_image_rotations("full")
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

    def move(self, interval):
        is_collision = False
        for r in Player.wall_rects:
            if self.rect.colliderect(r):
                if (self.speed != Constants.PLAYER_MIN_SPEED):
                    self.speed = Constants.PLAYER_MIN_SPEED
                    self.damage += 1
                    self.crash.play()
                if (self.direction == "up"):
                    self.rect = self.rect.move(0, 3)
                if (self.direction == "down"):
                    self.rect = self.rect.move(0, -3)
                if (self.direction == "left"):
                    self.rect = self.rect.move(3, 0)
                if (self.direction == "right"):
                    self.rect = self.rect.move(-3, 0)
                if (self.direction == "upleft"):
                    self.rect = self.rect.move(3, 3)
                if (self.direction == "upright"):
                    self.rect = self.rect.move(-3, 3)
                if (self.direction == "downright"):
                    self.rect = self.rect.move(-3, -3)
                if (self.direction == "downleft"):
                    self.rect = self.rect.move(3, -3)
                is_collision = True

        if self.direction == "upleft":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.left - self.speed * interval) > 0 and (
                    self.rect.top - self.speed * interval) > 0:
                # no collision, move
                self.rect = self.rect.move(-self.speed * interval,
                                           -self.speed * interval)
            Player.last_move_1 = "upleft"
        if self.direction == "downleft":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.left - self.speed * interval) > 0 and (
                    self.rect.bottom + self.speed * interval) < \
                    self.screen_height:
                self.rect = self.rect.move(-self.speed * interval,
                                           +self.speed * interval)
            Player.last_move_1 = "downleft"
        if self.direction == "left":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.left - self.speed * interval) > 0:
                self.rect = self.rect.move(-self.speed * interval, 0)
            Player.last_move_1 = "left"
        if self.direction == "upright":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (
                    self.rect.right + self.speed * interval) < \
                    self.screen_width \
                    and (
                        self.rect.top) > 0:
                self.rect = self.rect.move(self.speed * interval,
                                           -self.speed * interval)
            Player.last_move_1 = "upright"
        if self.direction == "downright":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (
                    self.rect.right + self.speed * interval) < \
                    self.screen_width \
                    and (
                        self.rect.bottom + self.speed * interval) < \
                    self.screen_height:
                self.rect = self.rect.move(self.speed * interval,
                                           self.speed * interval)
            Player.last_move_1 = "downright"
        if self.direction == "right":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.right + self.speed * interval) < self.screen_width:
                self.rect = self.rect.move(self.speed * interval, 0)
            Player.last_move_1 = "right"
        if self.direction == "up":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.top - self.speed * interval) > 0:
                self.rect = self.rect.move(0, -self.speed * interval)
            Player.last_move_1 = "up"
        if self.direction == "down":
            if (
                is_collision and
                    (Player.last_move_1 in self.direction)):
                print('stop')
            elif (self.rect.bottom + self.speed * interval) < \
                    self.screen_height:
                self.rect = self.rect.move(0, self.speed * interval)
            Player.last_move_1 = "down"

    def add_walls(self, wrects):
        Player.wall_rects = wrects

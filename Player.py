import pygame as game


class Player(game.sprite.Sprite):
    # These are the images, images are default
    image = None
    crash = None
    STARTING_HEALTH = 100
    current = None

    # Constructor for our Player takes an initial location, the dimensions of
    # the screen, and the speed
    def __init__(self, location, screensize, speed, difficulty):
        game.sprite.Sprite.__init__(self)
        Player.screen_width = screensize[0]
        Player.screen_height = screensize[1]
        self.direction = "right"

        # set the images to the appropriate ones based on the direction of the
        # character
        if Player.image is None:
            self.set_image_rotations("images/playerfullhealth.png")
        if Player.crash is None:
            Player.crash = game.mixer.Sound("audio/car_screech.wav")

        # initialize
        self.image = Player.image
        self.crash = Player.crash
        self.damage = 0
        self.health = Player.STARTING_HEALTH
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.screen_width = Player.screen_width
        self.screen_height = Player.screen_height
        self.dir_changed = False
        self.difficulty = difficulty

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

            # check for collision with top or left
            if (self.rect.left - self.speed * interval) > 0 and (
                self.rect.top - self.speed * interval) > 0:
                # no collision, move
                self.rect = self.rect.move(-self.speed * interval,
                                           -self.speed * interval)

            # collision!
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_LEFT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downleft":
                self.dir_changed = True
                self.set_direction("downleft")
                self.crash.stop()
            if (self.rect.left - self.speed * interval) > 0 and (
                    self.rect.bottom + self.speed * interval) < \
                    self.screen_height:
                self.rect = self.rect.move(-self.speed * interval,
                                           +self.speed * interval)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_LEFT]:
            if self.direction != "left":
                self.dir_changed = True
                self.set_direction("left")
                self.crash.stop()
            if (self.rect.left - self.speed * interval) > 0:
                self.rect = self.rect.move(-self.speed * interval, 0)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_UP]:
            if self.direction != "upright":
                self.dir_changed = True
                self.set_direction("upright")
                self.crash.stop()
            if (
                        self.rect.right + self.speed * interval) < \
                    self.screen_width \
                    and (
                            self.rect.top) > 0:
                self.rect = self.rect.move(self.speed * interval,
                                           -self.speed * interval)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_RIGHT] and keys_pressed[game.K_DOWN]:
            if self.direction != "downright":
                self.dir_changed = True
                self.set_direction("downright")
                self.crash.stop()
            if (
                        self.rect.right + self.speed * interval) < \
                    self.screen_width \
                    and (
                                self.rect.bottom + self.speed * interval) < \
                            self.screen_height:
                self.rect = self.rect.move(self.speed * interval,
                                           self.speed * interval)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_RIGHT]:
            if self.direction != "right":
                self.dir_changed = True
                self.set_direction("right")
                self.crash.stop()
            if (self.rect.right + self.speed * interval) < self.screen_width:
                self.rect = self.rect.move(self.speed * interval, 0)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_UP]:
            if self.direction != "up":
                self.dir_changed = True
                self.set_direction("up")
                self.crash.stop()
            if (self.rect.top - self.speed * interval) > 0:
                self.rect = self.rect.move(0, -self.speed * interval)
            else:
                self.damage += 1
                self.crash.play()

        elif keys_pressed[game.K_DOWN]:
            if self.direction != "down":
                self.dir_changed = True
                self.set_direction("down")
                self.crash.stop()
            if (self.rect.bottom + self.speed * interval) < self.screen_height:
                self.rect = self.rect.move(0, self.speed * interval)
            else:
                self.damage += 1
                self.crash.play()

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
        self.health = self.STARTING_HEALTH - (
            self.damage / (10 * (11 - self.difficulty)))
        if self.health < 25 and not self.current == "quarter":
            self.current = "quarter"
            self.set_image_rotations("images/playerquarterhealth.png")
        elif 25 < self.health < 75 and not self.current == \
                "half":
            self.current = "half"
            self.set_image_rotations("images/playerhalfhealth.png")
        elif self.health > 75 and not self.current == "full":
            self.current = "full"
            self.set_image_rotations("images/playerfullhealth.png")
        return self.health

    def set_image_rotations(self, imageloc):
        Player.image = game.image.load(imageloc)
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

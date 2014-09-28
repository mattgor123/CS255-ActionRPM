import pygame as game
import util.SpriteSheet as SP


class Enemy(game.sprite.Sprite):
    image = None
    screen_width = 0
    screen_height = 0
    should_change_motion_direction = False
    FRAME_SLOW = 10

    # Enemy constructor takes an initial location, screendims for collisions,
    # a speed, and a starting direction
    def __init__(self, location, screensize, speed, direction):
        game.sprite.Sprite.__init__(self)
        self.direction = direction
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

        # set the image based on the direction
        if direction == 1:
            self.set_direction("right")
            self.moving_direction = "right"
        elif direction == 2:
            self.set_direction("downright")
            self.moving_direction = "downright"
        elif direction == 3:
            self.set_direction("down")
            self.moving_direction = "down"
        elif direction == 4:
            self.set_direction("downleft")
            self.moving_direction = "downleft"
        elif direction == 5:
            self.set_direction("left")
            self.moving_direction = "left"
        elif direction == 6:
            self.set_direction("upleft")
            self.moving_direction = "upleft"
        elif direction == 7:
            self.set_direction("up")
            self.moving_direction = "up"
        elif direction == 8:
            self.set_direction("upright")
            self.moving_direction = "upright"
        self.set_image()
        #set the speed & get the rectangle
        self.speed = speed
        self.rect = self.image.get_rect()
        #make sure it is in the appropriate location
        self.rect.topleft = location
        #get the width & height of screen
        self.width = screensize[0]
        self.height = screensize[1]

    # this is the update method with a parameter - it ensures the Enemy is
    # facing opposite dir of the Player then updates
    def update(self, dir_changed, direction, interval):
        if dir_changed:
            if direction == "right" and self.direction != "left":
                self.set_direction("left")
            elif direction == "downright" and self.direction != "upleft":
                self.set_direction("upleft")
            elif direction == "down" and self.direction != "up":
                self.set_direction("up")
            elif direction == "downleft" and self.direction != "upright":
                self.set_direction("upright")
            elif direction == "left" and self.direction != "right":
                self.set_direction("right")
            elif direction == "upleft" and self.direction != "downright":
                self.set_direction("downright")
            elif direction == "up" and self.direction != "down":
                self.set_direction("down")
            elif direction == "upright" and self.direction != "downleft":
                self.set_direction("downleft")
        self.set_image()
        self.move(interval, Enemy.should_change_motion_direction)

    #this moves the Enemy to where he is supposed to be based on the direction
    '''
    Note : We wrote this function interpreting 'look' to mean the direction
    in which the Enemy is facing.
    Please have pity on our souls for the duplicated/relatively ugly
    code...not currently being used.
    '''
    def move(self, interval, should_move_in_dir_facing):
        if should_move_in_dir_facing:
            if self.direction == "upleft":
                self.rect = self.rect.move(-self.speed * interval,
                                           -self.speed * interval)
                #Two possible collisions are top & left (or corner)
                if self.rect.top < 0 and self.rect.left < 0:
                    self.set_direction("downright")
                elif self.rect.top < 0:
                    self.set_direction("downleft")
                elif self.rect.left < 0:
                    self.set_direction("upright")

            elif self.direction == "downleft":
                self.rect = self.rect.move(-self.speed * interval,
                                           +self.speed * interval)
                #Two possible collisions are bottom & left (or corner)
                if self.rect.bottom > self.screen_height and self.rect.left \
                        < 0:
                    self.set_direction("upright")
                elif self.rect.bottom > self.screen_height:
                    self.set_direction("upleft")
                elif self.rect.left < 0:
                    self.set_direction("downright")

            elif self.direction == "upright":
                self.rect = self.rect.move(self.speed * interval,
                                           -self.speed * interval)
                #Two possible collisions are top & right (or corner)
                if self.rect.top < 0 and self.rect.right > self.screen_width:
                    self.set_direction("downleft")
                elif self.rect.top < 0:
                    self.set_direction("downright")
                elif self.rect.right > self.screen_width:
                    self.set_direction("upleft")

            elif self.direction == "downright":
                self.rect = self.rect.move(self.speed * interval,
                                           self.speed * interval)
                #Two possible collisions are bottom & right (or corner)
                if self.rect.bottom > self.screen_height and self.rect.right \
                        > self.screen_width:
                    self.set_direction("upleft")
                elif self.rect.bottom > self.screen_height:
                    self.set_direction("upright")
                elif self.rect.right > self.screen_width:
                    self.set_direction("downleft")

            elif self.direction == "right":
                self.rect = self.rect.move(self.speed * interval, 0)
                #Only possible collision is to the right
                if self.rect.right > self.screen_width:
                    self.set_direction("left")

            elif self.direction == "up":
                self.rect = self.rect.move(0, -self.speed * interval)
                #Only possible collision is top
                if self.rect.top < 0:
                    self.set_direction("down")

            elif self.direction == "down":
                self.rect = self.rect.move(0, self.speed * interval)
                #Only possible collision is bottom
                if self.rect.bottom > self.screen_height:
                    self.set_direction("up")

            elif self.direction == "left":
                self.rect = self.rect.move(-self.speed * interval, 0)
                #Only possible collision is left
                if self.rect.left < 0:
                    self.set_direction("right")
        else:
            self.move_based_on_initial_dir(interval)

    #method to move based on the initialdirection rather than currently facing
    def move_based_on_initial_dir(self, interval):
        if self.moving_direction == "upleft":
            self.rect = self.rect.move(-self.speed * interval,
                                       -self.speed * interval)
            #Two possible collisions are top & left (or corner)
            if self.rect.top < 0 and self.rect.left < 0:
                self.moving_direction = "downright"
            elif self.rect.top < 0:
                self.moving_direction = "downleft"
            elif self.rect.left < 0:
                self.moving_direction = "upright"

        elif self.moving_direction == "downleft":
            self.rect = self.rect.move(-self.speed * interval,
                                       +self.speed * interval)
            #Two possible collisions are bottom & left (or corner)
            if self.rect.bottom > self.screen_height and self.rect.left < 0:
                self.moving_direction = "upright"
            elif self.rect.bottom > self.screen_height:
                self.moving_direction = "upleft"
            elif self.rect.left < 0:
                self.moving_direction = "downright"

        elif self.moving_direction == "upright":
            self.rect = self.rect.move(self.speed * interval,
                                       -self.speed * interval)
            #Two possible collisions are top & right (or corner)
            if self.rect.top < 0 and self.rect.right > self.screen_width:
                self.moving_direction = "downleft"
            elif self.rect.top < 0:
                self.moving_direction = "downright"
            elif self.rect.right > self.screen_width:
                self.moving_direction = "upleft"

        elif self.moving_direction == "downright":
            self.rect = self.rect.move(self.speed * interval,
                                       self.speed * interval)
            #Two possible collisions are bottom & right (or corner)
            if self.rect.bottom > self.screen_height and self.rect.right > \
                    self.screen_width:
                self.moving_direction = "upleft"
            elif self.rect.bottom > self.screen_height:
                self.moving_direction = "upright"
            elif self.rect.right > self.screen_width:
                self.moving_direction = "downleft"

        elif self.moving_direction == "right":
            self.rect = self.rect.move(self.speed * interval, 0)
            #Only possible collision is to the right
            if self.rect.right > self.screen_width:
                self.moving_direction = "left"

        elif self.moving_direction == "up":
            self.rect = self.rect.move(0, -self.speed * interval)
            #Only possible collision is top
            if self.rect.top < 0:
                self.moving_direction = "down"

        elif self.moving_direction == "down":
            self.rect = self.rect.move(0, self.speed * interval)
            #Only possible collision is bottom
            if self.rect.bottom > self.screen_height:
                self.moving_direction = "up"

        elif self.moving_direction == "left":
            self.rect = self.rect.move(-self.speed * interval, 0)
            #Only possible collision is left
            if self.rect.left < 0:
                self.moving_direction = "right"

    #method to set the direction
    def set_direction(self, direction):
        #set the image based on the direction
        if direction == "right":
            self.IMAGES = Enemy.right
            if Enemy.should_change_motion_direction:
                self.direction = "right"
        elif direction == "downright":
            self.IMAGES = Enemy.downright
            if Enemy.should_change_motion_direction:
                self.direction = "downright"
        elif direction == "down":
            self.IMAGES = Enemy.down
            if Enemy.should_change_motion_direction:
                self.direction = "down"
        elif direction == "downleft":
            self.IMAGES = Enemy.downleft
            if Enemy.should_change_motion_direction:
                self.direction = "downleft"
        elif direction == "left":
            self.IMAGES = Enemy.left
            if Enemy.should_change_motion_direction:
                self.direction = "left"
        elif direction == "upleft":
            self.IMAGES = Enemy.upleft
            if Enemy.should_change_motion_direction:
                self.direction = "upleft"
        elif direction == "up":
            self.IMAGES = Enemy.up
            if Enemy.should_change_motion_direction:
                self.direction = "up"
        elif direction == "upright":
            self.IMAGES = Enemy.upright
            if Enemy.should_change_motion_direction:
                self.direction = "upright"

    def set_image(self):
        self.image = self.IMAGES[self.frame]
        self.frameCalls += 1
        if self.frameCalls % Enemy.FRAME_SLOW == 0:
            self.frame += 1

        if self.frame == len(self.IMAGES):
            self.frame = 0

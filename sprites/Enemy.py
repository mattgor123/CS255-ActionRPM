import pygame as game
import util.SpriteSheet as SP
from math import fabs


class Enemy(game.sprite.Sprite):
    image = None
    screen_width = 0
    screen_height = 0
    should_change_motion_direction = False
    FRAME_SLOW = 10

    # Enemy constructor takes an initial location, screendims for collisions,
    # a speed, and a starting direction
    def __init__(self, location, screensize, temp_map, speed, direction, move_array):
        global map
        map = temp_map

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

    # this is the update method with a parameter - it ensures the Enemy is
    # facing opposite dir of the Player then updates
    def update(self, interval):
        self.move(interval)

    def get_strength(self):
        return 10
    #this moves the Enemy to where he is supposed to be based on the direction
    '''
    Note : We wrote this function interpreting 'look' to mean the direction
    in which the Enemy is facing.
    Please have pity on our souls for the duplicated/relatively ugly
    code...not currently being used.
    '''
    def move(self, interval):

        curr_action = self.movements[self.current_move]
        distance_moved_x = fabs(self.old_pos_x - self.x)
        distance_moved_y = fabs(self.old_pos_y - self.y)

        if(curr_action[0:1] == "d"):
            self.y += self.speed*interval
            self.direction = "down"
            self.set_direction("down")
            if distance_moved_y > float(curr_action[1:]):
                if(self.current_move == len(self.movements)-1):
                    self.current_move = 0
                else:
                    self.current_move += 1
                self.old_pos_y = self.y


        elif(curr_action[0:1] == "r"):
            self.x += self.speed*interval
            self.direction = "right"
            self.set_direction("right")
            if distance_moved_x > float(curr_action[1:]):
                if(self.current_move == len(self.movements)-1):
                    self.current_move = 0
                else:
                    self.current_move += 1
                self.old_pos_x = self.x


        elif(curr_action[0:1] == "u"):
            self.y -= self.speed*interval
            self.direction = "up"
            self.set_direction("up")
            if distance_moved_y > float(curr_action[1:]):
                if(self.current_move == len(self.movements)-1):
                    self.current_move = 0
                else:
                    self.current_move += 1
                self.old_pos_y = self.y


        elif(curr_action[0:1] == "l"):
            self.direction = "left"
            self.set_direction("left")
            self.x -= self.speed*interval
            if distance_moved_x > float(curr_action[1:]):
                if(self.current_move == len(self.movements)-1):
                    self.current_move = 0
                else:
                    self.current_move += 1
                self.old_pos_x = self.x



    """
        if self.direction == "right":
            self.x += self.speed*interval
            if self.x > 42.9:
                self.direction = "left"
                self.set_direction("left")

        elif self.direction == "up":
            self.y -= self.speed*interval
            if self.y <= 3.1:
                self.direction = "down"
                self.set_direction("down")

        elif self.direction == "down":
            self.y += self.speed*interval
            if self.y > 7:
                self.direction = "right"
                self.set_direction("right")

        elif self.direction == "left":
            self.x -= self.speed*interval
            if self.x <= 39:
                self.direction = "up"
                self.set_direction("up") """

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
        self.image = self.IMAGES[self.frame]
        self.frameCalls += 1
        if self.frameCalls % Enemy.FRAME_SLOW == 0:
            self.frame += 1

        if self.frame == len(self.IMAGES):
            self.frame = 0

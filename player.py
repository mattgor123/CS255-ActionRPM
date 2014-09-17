import pygame as game

class player(game.sprite.Sprite):
    #These are the images, images are default
    image = None
    screenwidth = 0
    screenheight = 0

    #Constructor for our player takes an initial location, the dimensions of the screen, and the speed
    def __init__(self, location, screensize, speed):
        game.sprite.Sprite.__init__(self)
        player.screenwidth = screensize[0]
        player.screenheight = screensize[1]
        #set the images to the appropriate ones based on the direction of the character
        if player.image is None:
            player.image = game.image.load("images/playerfullhealth.png")
            player.right = player.image
            player.left  = game.transform.rotate(player.right, 180)
            player.up  = game.transform.rotate(player.right, 90)
            player.down  = game.transform.rotate(player.right, -90)
            player.upright  = game.transform.rotate(player.right, 45)
            player.upleft  = game.transform.rotate(player.right, 135)
            player.downright  = game.transform.rotate(player.right, -45)
            player.downleft  = game.transform.rotate(player.right, -135)

        #initialize
        self.image = player.image
        self.speed = speed
        self.direction = "right"
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.screenwidth = screensize[0]
        self.screenheight = screensize[1]

    #update method moves the sprite & possibly changes its image based on the keypress
    def update(self):
        keysPressed = game.key.get_pressed()
        if keysPressed[game.K_LEFT] and keysPressed[game.K_UP]:
            #check for collision with top or left
            if (self.rect.left-self.speed) > 0 and (self.rect.top-self.speed) > 0:
                #no collision, move
                self.rect =  self.rect.move(-self.speed,-self.speed)
                if self.direction != "upleft":
                    self.setdirection("upleft")
            else:
                print("collision top left")
                #damage counter increase maybe?
        elif keysPressed[game.K_LEFT] and keysPressed[game.K_DOWN]:
            if (self.rect.left-self.speed) > 0 and (self.rect.bottom + self.speed) < self.screenheight:
                self.rect =  self.rect.move(-self.speed,+self.speed)
                if self.direction != "downleft":
                    self.setdirection("downleft")
            else:
                print("collision downleft")
        elif keysPressed[game.K_LEFT]:
            if (self.rect.left-self.speed) > 0:
                self.rect =  self.rect.move(-self.speed,0)
                if self.direction != "left":
                    self.setdirection("left")
            else:
                print("collision left")
        elif keysPressed[game.K_RIGHT] and keysPressed[game.K_UP]:
            if (self.rect.right+self.speed) < self.screenwidth and (self.rect.top) > 0:
                self.rect =  self.rect.move(self.speed,-self.speed)
                if self.direction != "upright":
                    self.setdirection("upright")
            else:
                print("collision topright")
        elif keysPressed[game.K_RIGHT] and keysPressed[game.K_DOWN]:
            if (self.rect.right+self.speed) < self.screenwidth and (self.rect.bottom + self.speed) < self.screenheight:
                self.rect =  self.rect.move(self.speed,self.speed)
                if self.direction != "downright":
                    self.setdirection("downright")
            else:
                print("collision bottomright")
        elif keysPressed[game.K_RIGHT]:
            if (self.rect.right + self.speed) < self.screenwidth:
                self.rect =  self.rect.move(self.speed,0)
                if self.direction != "right":
                    self.setdirection("right")
            else:
                print("collision right")

        elif keysPressed[game.K_UP]:
            if (self.rect.top - self.speed) > 0:
                self.rect =  self.rect.move(0,-self.speed)
                if self.direction != "up":
                    self.setdirection("up")
            else:
                print("collision top")
        elif keysPressed[game.K_DOWN]:
            if (self.rect.bottom + self.speed) < self.screenheight:
                self.rect =  self.rect.move(0,self.speed)
                if self.direction != "down":
                    self.setdirection("down")
            else:
                print("collision bottom")

    def setdirection(self, direction):
        self.direction=direction
        #set the image based on the direction
        if (direction == "right"):
            self.image = player.right
        elif (direction == "downright"):
            self.image = player.downright
        elif (direction == "down"):
            self.image = player.down
        elif (direction == "downleft"):
            self.image = player.downleft
        elif (direction == "left"):
            self.image = player.left
        elif (direction == "upleft"):
            self.image = player.upleft
        elif (direction == "up"):
            self.image = player.up
        elif (direction == "upright"):
            self.image = player.upright
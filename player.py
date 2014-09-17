import pygame as game

class player(game.sprite.Sprite):
    #These are the images, images are default
    image = None
    crash = None
    startinghealth = 100
    current = None

    #Constructor for our player takes an initial location, the dimensions of the screen, and the speed
    def __init__(self, location, screensize, speed, difficulty):
        game.sprite.Sprite.__init__(self)
        player.screenwidth = screensize[0]
        player.screenheight = screensize[1]
        self.direction="right"

        #set the images to the appropriate ones based on the direction of the character
        if player.image is None:
            self.setimgrotations("images/playerfullhealth.png")
        if player.crash is None:
            player.crash = game.mixer.Sound("audio/car_screech.wav")

        #initialize
        self.image = player.image
        self.crash = player.crash
        self.damage = 0
        self.health = player.startinghealth
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.screenwidth = screensize[0]
        self.screenheight = screensize[1]
        self.dirchanged = False
        self.difficulty = difficulty

    #update method moves the sprite & possibly changes its image based on the keypress
    def update(self,interval):
        self.dirchanged = False
        keysPressed = game.key.get_pressed()
        if keysPressed[game.K_LEFT] and keysPressed[game.K_UP]:
            #change of direction, stop playing crash sound & set the direction
            if self.direction != "upleft":
                self.dirchanged = True
                self.setdirection("upleft")
                self.crash.stop()

            #check for collision with top or left
            if (self.rect.left-self.speed*interval) > 0 and (self.rect.top-self.speed*interval) > 0:
                #no collision, move
                self.rect =  self.rect.move(-self.speed*interval,-self.speed*interval)

            #collision!
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_LEFT] and keysPressed[game.K_DOWN]:
            if self.direction != "downleft":
                self.dirchanged = True
                self.setdirection("downleft")
                self.crash.stop()
            if (self.rect.left-self.speed*interval) > 0 and (self.rect.bottom + self.speed*interval) < self.screenheight:
                self.rect =  self.rect.move(-self.speed*interval,+self.speed*interval)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_LEFT]:
            if self.direction != "left":
                self.dirchanged = True
                self.setdirection("left")
                self.crash.stop()
            if (self.rect.left-self.speed*interval) > 0:
                self.rect =  self.rect.move(-self.speed*interval,0)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_RIGHT] and keysPressed[game.K_UP]:
            if self.direction != "upright":
                self.dirchanged = True
                self.setdirection("upright")
                self.crash.stop()
            if (self.rect.right+self.speed*interval) < self.screenwidth and (self.rect.top) > 0:
                self.rect =  self.rect.move(self.speed*interval,-self.speed*interval)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_RIGHT] and keysPressed[game.K_DOWN]:
            if self.direction != "downright":
                self.dirchanged = True
                self.setdirection("downright")
                self.crash.stop()
            if (self.rect.right+self.speed*interval) < self.screenwidth and (self.rect.bottom + self.speed*interval) < self.screenheight:
                self.rect =  self.rect.move(self.speed*interval,self.speed*interval)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_RIGHT]:
            if self.direction != "right":
                self.dirchanged = True
                self.setdirection("right")
                self.crash.stop()
            if (self.rect.right + self.speed*interval) < self.screenwidth:
                self.rect =  self.rect.move(self.speed*interval,0)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_UP]:
            if self.direction != "up":
                self.dirchanged = True
                self.setdirection("up")
                self.crash.stop()
            if (self.rect.top - self.speed*interval) > 0:
                self.rect =  self.rect.move(0,-self.speed*interval)
            else:
                self.damage+=1
                self.crash.play()

        elif keysPressed[game.K_DOWN]:
            if self.direction != "down":
                self.dirchanged = True
                self.setdirection("down")
                self.crash.stop()
            if (self.rect.bottom + self.speed*interval) < self.screenheight:
                self.rect =  self.rect.move(0,self.speed*interval)
            else:
                self.damage+=1
                self.crash.play()

    def setdirection(self, direction):
        self.direction=direction
        #set the image based on the direction
        if (direction == "right"):
            self.image = player.right
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "downright"):
            self.image = player.downright
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "down"):
            self.image = player.down
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "downleft"):
            self.image = player.downleft
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "left"):
            self.image = player.left
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "upleft"):
            self.image = player.upleft
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "up"):
            self.image = player.up
            self.rect = self.image.get_rect(center=self.rect.center)
        elif (direction == "upright"):
            self.image = player.upright
            self.rect = self.image.get_rect(center=self.rect.center)

    def calchealth(self):
        self.health = self.startinghealth - (self.damage / (10*(11-self.difficulty)))
        if self.health < 25 and not self.current == "quarter":
            self.current = "quarter"
            self.setimgrotations("images/playerquarterhealth.png")
        elif self.health > 25 and self.health < 75 and not self.current == "half":
            self.current = "half"
            self.setimgrotations("images/playerhalfhealth.png")
        elif self.health > 75 and not self.current == "full":
            self.current = "full"
            self.setimgrotations("images/playerfullhealth.png")
        return self.health

    def setimgrotations(self,imageloc):
        player.image = game.image.load(imageloc)
        player.rect = player.image.get_rect()
        player.right = player.image
        player.left  = game.transform.rotate(player.right, 180)
        player.up  = game.transform.rotate(player.right, 90)
        player.down  = game.transform.rotate(player.right, -90)
        player.upright  = game.transform.rotate(player.right, 45)
        player.upleft  = game.transform.rotate(player.right, 135)
        player.downright  = game.transform.rotate(player.right, -45)
        player.downleft  = game.transform.rotate(player.right, -135)
        self.setdirection(self.direction)



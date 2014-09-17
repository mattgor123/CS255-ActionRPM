import pygame as game

class player(game.sprite.Sprite):
	#These are the images, images are default
	image = None
	right = None
	left = None
	up = None
	down = None
	#Cannot be a decimal
	speed = 1
	direction = "right"

	def __init__(self, location):
		game.sprite.Sprite.__init__(self)

		if player.image is None:
			player.image = game.image.load("images/playerfullhealth.png")
			player.right = player.image
			player.left  = game.transform.rotate(player.right, 180)
			player.up  = game.transform.rotate(player.right, 90)
			player.down  = game.transform.rotate(player.right, -90)

		self.image = player.image

		self.rect = self.image.get_rect()
		self.rect.topleft = [300,0]

	def move(self):	
		#self.rect = self.rect.move(-5,0)
		keysPressed = game.key.get_pressed()
		if keysPressed[game.K_LEFT]:
			self.rect =  self.rect.move(-self.speed,0)
			if self.direction != "left":
				self.image = self.left
				self.direction = "left"
		if keysPressed[game.K_RIGHT]:
			self.rect =  self.rect.move(self.speed,0)
			if self.direction != "right":
				self.image = self.right
				self.direction = "right"
		if keysPressed[game.K_UP]:
			self.rect =  self.rect.move(0,-self.speed)
			if self.direction != "up":
				self.image = self.up
				self.direction = "up"
		if keysPressed[game.K_DOWN]:
			self.rect =  self.rect.move(0,self.speed)
			if self.direction != "down":
				self.image = self.down
				self.direction = "down"

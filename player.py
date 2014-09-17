import pygame as game

class player(game.sprite.Sprite):
	#These are the images, images are default
	image = None
	right = None
	left = None
	up = None
	down = None
	upright = None
	upleft = None
	downright = None
	downleft = None

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
			player.upright  = game.transform.rotate(player.right, 45)
			player.upleft  = game.transform.rotate(player.right, 135)
			player.downright  = game.transform.rotate(player.right, -45)
			player.downleft  = game.transform.rotate(player.right, -135)

		self.image = player.image

		self.rect = self.image.get_rect()
		self.rect.topleft = location

	def move(self):	
		#self.rect = self.rect.move(-5,0)
		keysPressed = game.key.get_pressed()
		if keysPressed[game.K_LEFT] and keysPressed[game.K_UP]:
			self.rect =  self.rect.move(-self.speed,-self.speed)
			if self.direction != "upleft":
				self.image = player.upleft
				self.direction = "upleft"
		elif keysPressed[game.K_LEFT] and keysPressed[game.K_DOWN]:
			self.rect =  self.rect.move(-self.speed,+self.speed)
			if self.direction != "downleft":
				self.image = player.downleft
				self.direction = "downleft"
		elif keysPressed[game.K_LEFT]:
			self.rect =  self.rect.move(-self.speed,0)
			if self.direction != "left":
				self.image = player.left
				self.direction = "left"
		elif keysPressed[game.K_RIGHT] and keysPressed[game.K_UP]:
			self.rect =  self.rect.move(self.speed,-self.speed)
			if self.direction != "upright":
				self.image = player.upright
				self.direction = "upright"
		elif keysPressed[game.K_RIGHT] and keysPressed[game.K_DOWN]:
			self.rect =  self.rect.move(self.speed,self.speed)
			if self.direction != "downright":
				self.image = player.downright
				self.direction = "downright"
		elif keysPressed[game.K_RIGHT]:
			self.rect =  self.rect.move(self.speed,0)
			if self.direction != "right":
				self.image = player.right
				self.direction = "right"
		elif keysPressed[game.K_UP]:
			self.rect =  self.rect.move(0,-self.speed)
			if self.direction != "up":
				self.image = player.up
				self.direction = "up"
		elif keysPressed[game.K_DOWN]:
			self.rect =  self.rect.move(0,self.speed)
			if self.direction != "down":
				self.image = player.down
				self.direction = "down"

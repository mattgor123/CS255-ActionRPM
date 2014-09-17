import pygame as game

class player(game.sprite.Sprite):
	image = None
	speed = .5

	def __init__(self, location):
		game.sprite.Sprite.__init__(self)

		if player.image is None:
			player.image = game.image.load("images/playerfullhealth.png")

		self.image = player.image

		self.rect = self.image.get_rect()
		self.rect.topleft = [300,0]

	def move(self):	
		#self.rect = self.rect.move(-5,0)
		keysPressed = game.key.get_pressed()
		if keysPressed[game.K_LEFT]:
			self.rect =  self.rect.move(-1,0)
		if keysPressed[game.K_RIGHT]:
			self.rect =  self.rect.move(1,0)
		if keysPressed[game.K_UP]:
			self.rect =  self.rect.move(0,-1)
		if keysPressed[game.K_DOWN]:
			self.rect =  self.rect.move(0,1)

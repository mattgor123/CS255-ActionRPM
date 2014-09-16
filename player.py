import pygame as game

class player(game.sprite.Sprite):

	def __init__(self):
		game.sprite.Sprite.__init__(self)

		self.image = game.image.load("./images/playerfullhealth.png").convert()

		self.image.set_colorkey(white)

		self.rect = self.image.get_rect()
